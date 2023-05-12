from scripts.factapi.DogAPI import DogAPI
from scripts.factapi.TranslatorService import TranslatorService
from scripts.http_utils import handle_http_errors


class FactService:
    def __init__(self):
        self.dog_api = DogAPI()
        self.translator_service = TranslatorService()

    @handle_http_errors
    def get_translated_fact(self, source_lang='en', target_lang='ru'):
        fact = self.dog_api.get_fact()
        if fact is not None:
            translated_fact = self.translator_service.translate(fact, source_lang, target_lang)
            return translated_fact
        else:
            return None
