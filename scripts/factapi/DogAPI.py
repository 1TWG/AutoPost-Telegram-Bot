import requests

from scripts.http_utils import handle_http_errors


class DogAPI:
    def __init__(self):
        self.url = 'https://dogapi.dog/api/v2/facts'

    @handle_http_errors
    def get_fact(self):
        response = requests.get(self.url)
        fact = response.json()['data'][0]['attributes']['body']
        return fact
