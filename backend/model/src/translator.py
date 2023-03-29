from transformers import pipeline

model_checkpoint = "Helsinki-NLP/opus-mt-en-ru"
translator = pipeline("translation", model=model_checkpoint)


def translate(text):
    return translator(text)[0]['translation_text']


if __name__ == '__main__':
    print(translate('This is my day'))
