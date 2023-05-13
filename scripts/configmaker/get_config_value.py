import configparser
import os

SETTINGS_FILE_PATH = 'settings.ini'


def get_config_value(section: str, option: str, prompt: str = None, type_hint=str):
    config = configparser.ConfigParser()
    if not os.path.exists(SETTINGS_FILE_PATH):
        with open(SETTINGS_FILE_PATH, 'w') as f:
            config.write(f)
    config.read(SETTINGS_FILE_PATH)
    value_str = config.get(section, option, fallback='')
    value = None
    if not value_str:
        if prompt is None:
            prompt = f'Введите значение для "{option}" в разделе "{section}": '
        while value is None:
            try:
                value = type_hint(input(prompt))
            except ValueError:
                print(f'Неверный тип значения. Ожидалось значение типа {type_hint.__name__}. Попробуйте еще раз.')
        config.set(section, option, str(value))
        with open(SETTINGS_FILE_PATH, 'w') as f:
            config.write(f)
    else:
        value = type_hint(value_str)
    return value


def set_config_value(section: str, option: str, value: str) -> None:
    config = configparser.ConfigParser()
    if not os.path.exists(SETTINGS_FILE_PATH):
        with open(SETTINGS_FILE_PATH, 'w') as f:
            config.write(f)
    config.read(SETTINGS_FILE_PATH)
    config.set(section, option, value)
    with open(SETTINGS_FILE_PATH, 'w') as f:
        config.write(f)
