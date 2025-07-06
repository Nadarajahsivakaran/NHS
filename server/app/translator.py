from deep_translator import GoogleTranslator

def translate_to_english(text, source_lang):
    if source_lang == "en":
        return text
    return GoogleTranslator(source=source_lang, target="en").translate(text)
