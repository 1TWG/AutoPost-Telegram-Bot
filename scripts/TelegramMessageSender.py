import telebot

from scripts.IMessageSender import IMessageSender


class TelegramMessageSender(IMessageSender):
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)

    def send_message(self, chat_id: str, text: str) -> None:
        self.bot.send_message(chat_id=chat_id, text=text)

    def send_animation(self, chat_id: str, animation, caption: str = ""):
        self.bot.send_video(chat_id, animation, caption=caption, parse_mode='Markdown')
