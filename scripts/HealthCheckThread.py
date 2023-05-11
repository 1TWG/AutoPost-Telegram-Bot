import threading


class HealthCheckThread:
    def __init__(self, service):
        self.service = service

    def start(self) -> None:
        threading.Thread(target=self.service.start).start()
