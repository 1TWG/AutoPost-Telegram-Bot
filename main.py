import time

import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from scripts.ActivateOnetimeSendingPost import ActivateOnetimeSendingPost
from scripts.HealthCheckService import HealthCheckService
from scripts.HealthCheckThread import HealthCheckThread
from scripts.StartCommandHandler import StartCommandHandler
from scripts.TelegramMessageSender import TelegramMessageSender

# Укажите здесь токен вашего бота, полученный от BotFather
TOKEN = '5229055040:AAGp21qFhH-1AAK3hQzb-xmu576CvfG-JTY'

# URL для health-check запросов
health_check_url = "http://example.com/health-check"

# Создаем экземпляры классов для отправки сообщений и обработки команд
message_sender = TelegramMessageSender(TOKEN)
start_handler = StartCommandHandler(message_sender=message_sender)
activate_onetime_send = ActivateOnetimeSendingPost(message_sender=message_sender)

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Флаг, указывающий, нужно ли продолжать отправлять сообщения
continue_sending = False


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
    channel_id = '@grab_chan'
    activate_onetime_send.handle(channel_id)


@bot.message_handler(func=lambda message: message.text == 'Активировать автопостинг')
def handle_activate_posting_command(message: telebot.types.Message) -> None:
    global continue_sending
    continue_sending = True
    # Установить интервал в секундах, через который нужно отправлять сообщения
    interval = 3600 / 30  # Один час
    while continue_sending:  # Остановить отправку при установке значения `continue_sending` в `False`
        channel_id = '@grab_chan'
        activate_onetime_send.handle(channel_id)
        time.sleep(interval)


@bot.message_handler(func=lambda message: message.text == 'Остановить автопостинг')
def handle_stop_posting_command(message: telebot.types.Message) -> None:
    global continue_sending  # Для работы со значением глобальной переменной
    continue_sending = False
    bot.send_message(message.chat.id, 'Автопостинг остановлен.')


# Создаем экземпляры классов и запускаем поток health-check проверок
service = HealthCheckService(health_check_url)
thread = HealthCheckThread(service)
thread.start()

# Запускаем бота
bot.delete_webhook()
bot.polling()
