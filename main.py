# main.py

import time

import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from scripts.ActivateOnetimeSendingPost import ActivateOnetimeSendingPost
from scripts.StartCommandHandler import StartCommandHandler
from scripts.TelegramMessageSender import TelegramMessageSender
from scripts.configmaker.get_config_value import get_config_value, set_config_value

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
    button_delay = KeyboardButton('Изменить задержку')
    markup.add(button_send, button_auto, button_stop, button_delay)
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
    interval = get_config_value('DEFAULT', 'PostDelay', type_hint=int)
    while continue_sending:
        activate_onetime_send.handle(CHANNEL_ID)
        time.sleep(interval)


@bot.message_handler(func=lambda message: message.text == 'Остановить автопостинг')
def handle_stop_posting_command(message: telebot.types.Message) -> None:
    global continue_sending  # Для работы со значением глобальной переменной
    continue_sending = False
    bot.send_message(message.chat.id, 'Автопостинг остановлен.')


@bot.message_handler(func=lambda message: message.text == 'Изменить задержку')
def handle_change_delay_command(message: telebot.types.Message) -> None:
    # Отправляем запрос на новое значение задержки
    bot.send_message(message.chat.id, 'Введите новое значение задержки (в секундах):')

    # Устанавливаем обработчик на следующее сообщение пользователя
    bot.register_next_step_handler(message, change_delay)


def change_delay(message: telebot.types.Message) -> None:
    try:
        new_delay = int(message.text)
        if new_delay > 0:
            set_config_value('DEFAULT', 'PostDelay', str(new_delay))
            bot.send_message(message.chat.id, f'Задержка успешно изменена на {new_delay} секунд.')
        else:
            bot.send_message(message.chat.id, 'Задержка должна быть положительным числом.')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат числа. Попробуйте еще раз.')


if __name__ == '__main__':
    bot.polling()
