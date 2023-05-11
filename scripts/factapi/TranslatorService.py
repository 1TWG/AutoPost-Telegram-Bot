from googletrans import Translator


class TranslatorService:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, source_lang, target_lang):
        translation = self.translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
