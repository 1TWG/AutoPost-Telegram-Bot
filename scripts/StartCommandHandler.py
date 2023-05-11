import telebot
from telebot import types

from scripts.IMessageSender import IMessageSender


class StartCommandHandler:
    def __init__(self, message_sender: IMessageSender):
        self.message_sender = message_sender

    def handle(self, message: telebot.types.Message) -> None:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        activate_channel_button = types.KeyboardButton(text="Активировать ведение канала")
        keyboard.add(activate_channel_button)

        self.message_sender.send_message(chat_id=str(message.chat.id),
                                         text="Привет! Я эхо-бот. Пришли мне что-нибудь и я повторю это.")
