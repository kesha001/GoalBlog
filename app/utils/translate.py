from translate import Translator
from langdetect import detect

def translate_text(text, from_lang, to_lang):
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(text)
    return translation


def detect_language(text):
    try:
        if isinstance(text, list):
            text = " ".join(text)
        detected_language = detect(text)
    except Exception as e:
        detected_language = None

    return detected_language