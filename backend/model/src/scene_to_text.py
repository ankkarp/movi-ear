from transformers import pipeline  # AutoProcessor, Blip2ForConditionalGeneration
from PIL import Image
import torch
import os
from tqdm import tqdm

# from summarizer.sbert import SBertSummarizer
# from summarizer import Summarizer

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
captioner = pipeline("image-to-text", model="ydshieh/vit-gpt2-coco-en", device=DEVICE)
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum", device=DEVICE)


# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def init_model():
#     processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
#     model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16).to(
#         DEVICE)
#     return processor, model


def summarize(text):
    # classifier = pipeline("summarization", model='sshleifer/distilbart-cnn-12-6')
    # model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
    # #model = Summarizer()
    # return model(text, num_sentences=2)

    return summarizer(text, min_length=5, max_length=15)[0]['summary_text']
    # return classifier(text, max_length=20, min_length=10)


# def blip(model, processor, path_to_image):
#     inputs = processor(Image.open(path_to_image), return_tensors="pt").to(DEVICE, torch.float16)
#     print(inputs)
#     generated_ids = model.generate(**inputs, max_new_tokens=20)
#     generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
#     return generated_text


def scene_to_text(path_to_scene_frames, translate=False):
    # model, processor = init_model()
    frames = sorted(os.listdir(path_to_scene_frames), key=lambda x: int(x[:x.find('.')]))
    text = ''
    # with tqdm(total=len(frames)) as pbar:
    for frame in frames:
        text += captioner(os.path.join(path_to_scene_frames, frame))[0][
            'generated_text']  # .strip().capitalize() + '. '
        # text += blip(model, processor, os.path.join(path_to_scene_frames, frame))
        # pbar.update(1)

    # print(text)

    return summarize(text)


if __name__ == '__main__':
    # main()
    # text_x = 'The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.'
    # print(summarizer(text_x, min_length=5, max_length=15)[0]['summary_text'])
    image_to_text('./test/frames3/folder1')
