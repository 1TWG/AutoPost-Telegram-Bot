from abc import ABC, abstractmethod


class IMessageSender(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, text: str) -> None:
        pass

    @abstractmethod
    def send_animation(self, chat_id: str, animation) -> None:
        pass
