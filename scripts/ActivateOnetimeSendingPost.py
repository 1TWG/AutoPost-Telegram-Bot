import logging
from io import BytesIO

import requests
import telebot

from scripts.IMessageSender import IMessageSender


class ActivateOnetimeSendingPost:
    def __init__(self, message_sender: IMessageSender):
        self.message_sender = message_sender

    def handle(self, message: telebot.types.Message) -> None:
        try:
            # Получаем случайный gif-файл с помощью API Giphy
            response = requests.get(
                'https://api.giphy.com/v1/gifs/random',
                params={'tag': 'dog', 'api_key': 'qUOOZIJMgv4UbZHSWh8tfgGhqNFZXKue'}
            )
            data = response.json()
            if not data or \
                    'data' not in data or \
                    'images' not in data['data'] or \
                    'original' not in data['data']['images'] or \
                    'mp4' not in data['data']['images']['original']:
                raise ValueError('Invalid response from Giphy API')
            image_url = data['data']['images']['original']['mp4']

            # Скачиваем gif-файл в память
            response = requests.get(image_url)
            response.raise_for_status()
            img_bytes = BytesIO(response.content)

            # Отправляем gif-файл пользователю
            self.send_animation(
                message.chat.id,
                img_bytes,
                f'\n[Пёсель](https://t.me/{message.chat.id})'
            )
        except Exception as e:
            logging.exception(f'Error sending GIF to chat {message.chat.id}: {e}')

    def send_animation(self, chat_id, animation_stream, caption=None):
        try:
            self.message_sender.send_animation(
                chat_id=chat_id,
                animation=animation_stream,
                caption=caption
            )
        except Exception as e:
            logging.exception(f'Error sending animation to chat {chat_id}: {e}')
