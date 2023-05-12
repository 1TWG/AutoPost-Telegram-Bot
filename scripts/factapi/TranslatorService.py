from googletrans import Translator

from scripts.http_utils import handle_http_errors


class TranslatorService:
    def __init__(self):
        self.translator = Translator()

    @handle_http_errors
    def translate(self, text, source_lang, target_lang):
        translation = self.translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
