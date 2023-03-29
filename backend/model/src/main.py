# from transformers import pipeline
#
# captions = [
#   {'start': 2.9, 'end': 25.2, 'sentence': 'A person is seen sitting on a table and leads into a woman speaking to the camera'},
#   {'start': 0.0, 'end': 61.9, 'sentence': 'A man is seen speaking to the camera and leads into several shots of people working on a building'},
#   {'start': 0.0, 'end': 12.7, 'sentence': 'A woman is sitting in a chair talking to the camera'},
#   {'start': 78.6, 'end': 100.0, 'sentence': 'The man then takes the cube and shows the cube off the table'},
#   {'start': 0.2, 'end': 5.2, 'sentence': 'A man is sitting on a chair with a woman sitting on a chair and talking'},
#   {'start': 38.8, 'end': 100.0, 'sentence': 'A man is seen speaking to the camera and leads into several shots of people working out and speaking to the camera'}
# ]
#
# a="Helsinki-NLP/opus-mt-en-ru"
# en_rus_translator = pipeline("translation", model=a)
# res = []
# for i in captions:
#     temp = {}
#     for k, v in i.items():
#         if k == 'sentence':
#             temp[k] = en_rus_translator(v)[0]['translation_text']
#         else:
#             temp[k] = v
#     res.append(temp)
#
# print(*res, sep='\n')

# from pytube import YouTube


from .vid_to_scenes import split_video_into_scenes
from .scene_to_text import scene_to_text
from .scene_into_frames import split_scene_into_frames
from .translator import translate
import warnings

from tqdm import tqdm
import os
import pandas as pd
import shutil
from .text_to_speech import text_to_speech
from datetime import datetime
import librosa
from pydub import AudioSegment
import subprocess

SCENES_FOLDER = 'scenes'
SCENES_FRAMES_FOLDER = 'scenes_frames'
AUDIO_FOLDER = 'audio_folder'
AUDIO_PATH = 'text_to_speech_folder'

os.environ['TOKENIZERS_PARALLELISM'] = 'False'


def pipeline(path_to_vid, save_path):
    # split vidio into scenes

    scenes_list = split_video_into_scenes(path_to_vid, dest_path=SCENES_FOLDER)

    # split each scene into frames
    scenes = sorted(os.listdir(SCENES_FOLDER), key=lambda x: int(x[:x.find('.')]))

    folder_names = []
    to_delete = []
    with tqdm(total=len(scenes)) as pbar:
        for i, vid in enumerate(scenes):
            current_video_path = os.path.join(SCENES_FOLDER, vid)

            # convert mp4 to wav

            #current_audio_path = extract_audio_file(current_video_path, path=AUDIO_FOLDER)

            # check scene audio

            # has_speech = detect_speech(current_audio_path)
            #
            # if has_speech:
            #     to_delete.append(i)
            #     pbar.update(1)
            #     continue

            folder_name = vid[:vid.find('.')]
            folder_names.append(folder_name)

            split_scene_into_frames(
                current_video_path,
                output_folder_path=os.path.join(SCENES_FRAMES_FOLDER, folder_name)
            )
            pbar.update(1)

    scenes_list[:] = [x for i, x in enumerate(scenes_list) if i not in to_delete]
    starts, ends = list(zip(*[(str(i[0]), str(i[1])) for i in scenes_list]))
    captions = []

    # generate and summarize text for each scene
    with tqdm(total=len(folder_names)) as pbar:
        for scene_folder in folder_names:
            captions.append(scene_to_text(os.path.join(SCENES_FRAMES_FOLDER, scene_folder)))
            pbar.update()

    translated_captions = []
    for i, caption in enumerate(captions):
        current_translated = translate(caption)
        translated_captions.append(current_translated)

    out_df = pd.DataFrame(
        {
            'start': starts,
            'end': ends,
            'caption': captions,
            'translated': translated_captions
        }
    )

    #out_df.to_csv('result10.csv', index=False)

    audio_duration_seconds = 0
    previous_start_seconds = 0

    combined = AudioSegment.empty()

    with tqdm(total=len(out_df)) as pbar:
        for idx, start_time, end_time, caption, ru_text in out_df.itertuples():
            # mean_text_lenght

            start_datetime = datetime.strptime(start_time, '%H:%M:%S.%f')
            start_seconds = (start_datetime - datetime(1900, 1, 1)).total_seconds()
            end_datetime = datetime.strptime(end_time, '%H:%M:%S.%f')
            end_seconds = (end_datetime - datetime(1900, 1, 1)).total_seconds()

            # speech.pause(time=f'{int((start_seconds - previous_start_seconds - audio_duration_seconds) * 1000)}ms')

            pause_duration = int((start_seconds - previous_start_seconds - audio_duration_seconds) * 1000)
            previous_start_seconds = start_seconds

            # audio_path = f'/content/audio_wav/{idx}_{start_time}.wav'
            combined = text_to_speech(
                ru_text,
                path=AUDIO_PATH,
                name=f'{idx}',
                pause_duration=pause_duration,
                combined=combined
            )
            current_audio = os.path.join(AUDIO_PATH, f'{idx}.wav')
            audio_duration_seconds = librosa.get_duration(path=current_audio)

            if audio_duration_seconds > (end_seconds - start_seconds):
                tem_path = os.path.join(AUDIO_PATH, 'temp.wav')
                cmd = f'ffmpeg -ss 0 -i {current_audio} -t {int(end_seconds - start_seconds)} {tem_path}'

                subprocess.call(cmd, shell=True)

                # audio_input = ffmpeg.input(current_audio)
                # audio_cut = audio_input.audio.filter('atrim', duration=end_seconds - start_seconds)
                # audio_output = ffmpeg.output(audio_cut, tem_path)
                # ffmpeg.run(audio_output)
                os.remove(current_audio)
                os.rename(tem_path, current_audio)
                # os.remove(tem_path)

            pbar.update(1)

    combined.export('final_audio.wav', format='wav')

    #shutil.rmtree(AUDIO_FOLDER)
    shutil.rmtree(SCENES_FOLDER)
    shutil.rmtree(SCENES_FRAMES_FOLDER)
    shutil.rmtree(AUDIO_PATH)

    input_video = path_to_vid

    print(input_video)

    input_audio = 'final_audio.wav'

    #command = f'ffmpeg -i {input_video} -filter:a "volume=0.5" output_1.mp4'
    command2 = f'ffmpeg -i {input_video} -i input_audio.wav -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 -shortest {save_path}'
    command5 = f'ffmpeg -i {input_audio} -filter:a "volume=4" input_audio.wav'

    #subprocess.call(command, shell=True)
    #print('command1 is done')
    subprocess.call(command5, shell=True)
    print('command5 is done')
    subprocess.call(command2, shell=True)
    print('command1 is done')

    os.remove(input_audio)
    #os.remove('output_1.mp4')
    os.remove('input_audio.wav')


if __name__ == '__main__':
    # yt = YouTube('https://www.youtube.com/watch?v=HtzPSh30f2A')
    # yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pipeline('../test/vid3.mp4')
    # import subprocess
    #
    # input_video = 'test/vid3.mp4'
    #
    # input_audio ='final_audio.wav'
    #
    # #ffmpeg.concat(input_video, input_audio, v=1, a=0).output('test/complete.mp4').run()
    # # out = ffmpeg.output(input_video, input_audio, 'test/complete1.mp4', vcodec='copy', acodec='aac', strict='experimental')
    # # out.run()
    #
    #
    #
    # command = f'ffmpeg -i {input_video} -filter:a "volume=0.5" output_1.mp4;'
    # command5 = f'ffmpeg -i {input_audio} -filter:a "volume=4" input_audio.wav;'
    #
    #
    # command1 = f'ffmpeg -i output_1.mp4 -i input_audio.wav -map 0 -map 1:a -c:v copy -shortest output.mp4'
    # command2 = f'ffmpeg -i output_1.mp4 -i input_audio.wav -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 -shortest output2.mp4'
    # command3 = f'ffmpeg -i output2.mp4 -filter:a "dynaudnorm=p=0.9:s=5" output2.mp4'
    # #command4 = f'ffmpeg -i output2.mp4 -filter:a loudnorm output2.mp4'
    # subprocess.call(command, shell=True)
    # subprocess.call(command5, shell=True)
    # subprocess.call(command2, shell=True)
    # #subprocess.call(command4, shell=True)

    # print(*scenes_list, sep='\n')
    # print(str(scenes_list[0][0]), str(scenes_list[0][1]))
