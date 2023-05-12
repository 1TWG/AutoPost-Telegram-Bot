# main.py

import time

import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from scripts.ActivateOnetimeSendingPost import ActivateOnetimeSendingPost
from scripts.StartCommandHandler import StartCommandHandler
from scripts.TelegramMessageSender import TelegramMessageSender
from scripts.configmaker.get_config_value import get_config_value

BOT_TOKEN = get_config_value('DEFAULT', 'BotToken', 'Введите токен бота: ')
CHANNEL_ID = get_config_value('DEFAULT', 'ChannelID', 'Введите ID канала: ')
POST_DELAY = get_config_value('DEFAULT', 'PostDelay', 'Введите периодичность публикации(сек): ', type_hint=int)
# Флаг, указывающий, нужно ли продолжать отправлять сообщения
continue_sending = False

# Создаем экземпляры классов для отправки сообщений и обработки команд
message_sender = TelegramMessageSender(BOT_TOKEN)
start_handler = StartCommandHandler(message_sender=message_sender)
activate_onetime_send = ActivateOnetimeSendingPost(message_sender=message_sender)

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start_command(message: telebot.types.Message) -> None:
    start_handler.handle(message)
    # Добавляем кнопки "Отправить сообщение в канал" и "Активировать автопостинг"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_send = KeyboardButton('Отправить сообщение в канал')
    button_auto = KeyboardButton('Активировать автопостинг')
    button_stop = KeyboardButton('Остановить автопостинг')
    markup.add(button_send, button_auto, button_stop)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


# Обработчик команды "Отправить сообщение в канал"
@bot.message_handler(func=lambda message: message.text == 'Отправить сообщение в канал')
def handle_activate_channel_command(message: telebot.types.Message) -> None:
    activate_onetime_send.handle(CHANNEL_ID)


@bot.message_handler(func=lambda message: message.text == 'Активировать автопостинг')
def handle_activate_posting_command(message: telebot.types.Message) -> None:
    global continue_sending
    continue_sending = True
    # Установить интервал в секундах, через который нужно отправлять сообщения
    interval = POST_DELAY
    while continue_sending:
        activate_onetime_send.handle(CHANNEL_ID)
        time.sleep(interval)


@bot.message_handler(func=lambda message: message.text == 'Остановить автопостинг')
def handle_stop_posting_command(message: telebot.types.Message) -> None:
    global continue_sending  # Для работы со значением глобальной переменной
    continue_sending = False
    bot.send_message(message.chat.id, 'Автопостинг остановлен.')


bot.polling()
