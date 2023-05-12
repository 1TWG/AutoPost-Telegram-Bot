import requests


def handle_http_errors(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            raise e

    return wrapper
