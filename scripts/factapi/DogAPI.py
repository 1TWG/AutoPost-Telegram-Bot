import requests


class DogAPI:
    def __init__(self):
        self.url = 'https://dogapi.dog/api/v2/facts'

    def get_fact(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            fact = response.json()['data'][0]['attributes']['body']
            return fact
        else:
            return None
