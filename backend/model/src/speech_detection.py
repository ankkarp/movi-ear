import whisper
import torch
import os
import numpy as np

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

device = "cuda" if torch.cuda.is_available() else "cpu"

# USE_ONNX = False  # change this to True if you want to test onnx model
# SAMPLING_RATE = 16000

# model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
#                               model='silero_vad',
#                               force_reload=True,
#                               onnx=USE_ONNX)

# (get_speech_timestamps,
#  save_audio,
#  read_audio,
#  VADIterator,
#  collect_chunks) = utils


# def detect_speech(path):
#     wav = read_audio(path, sampling_rate=SAMPLING_RATE)
#     # get speech timestamps from full audio file
#     speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE, return_seconds=True)
#     pprint(speech_timestamps)

model = whisper.load_model("medium", device=device)


def detect_speech(path_to_audio, threshold=0.64, len_threshold=1, language='en'):
    # audio = whisper.load_audio(path_to_audio)
    # audio = whisper.pad_or_trim(audio)
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    #
    # # _, probs = model.detect_language(mel)
    # # print(f"Detected language: {max(probs, key=probs.get)}")
    #
    # options = whisper.DecodingOptions(language=language)
    # result = whisper.decode(model, mel, options)
    # #print(result.text)
    # return result.no_speech_prob <= threshold and len(result.text) > len_threshold

    result = model.transcribe(path_to_audio, language=language)
    # print(result)
    # print('segments' in result.keys())
    # print(result.keys())
    if 'segments' in result.keys() and len(result['segments']) > 0:
        mean_prob = np.array([result['segments'][i]['no_speech_prob'] for i in range(len(result['segments']))]).mean()
        # print(mean_prob)
        return mean_prob <= threshold and len(result['text']) > len_threshold
    #     if 'no_speech_prob' in result['segments'][0].keys():
    #         return result['segments'][0]['no_speech_prob'] <= threshold
    # #return len(result['text']) > len_threshold
    # return True


if __name__ == '__main__':
    # detect_speech('audio_folder/002.wav'))
    # print(model.transcribe('audio_folder/vid5.wav', language='ru'))
    detect_speech('audio_folder/vid5.wav')
    # detect_speech(path='audio_folder/vid3.wav')
