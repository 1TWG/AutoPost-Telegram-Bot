import requests
import time


class HealthCheckService:
    def __init__(self, url):
        self.url = url

    def start(self) -> None:
        while True:
            try:
                # Отправляем GET-запрос на URL
                response = requests.get(self.url)
                if response.status_code == 200:
                    print("Health check OK")
            except Exception as e:
                print("Health check failed:", str(e))

            # Ждем 5 минут перед отправкой следующего запроса
            time.sleep(300)
