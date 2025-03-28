import asyncio
import time
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
import schedule

import config
import parser_mail
import to_exel
import parser_userside

# Объект бота
bot = Bot(token=config.BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()


# Создадим папки для хранения отчетов, если их нет
def create_folder():
    if not os.path.exists(f"TOEast"):
        os.makedirs(f"TOEast")
    if not os.path.exists(f"TOEast/list"):
        os.makedirs(f"TOEast/list")
    if not os.path.exists(f"TOWest"):
        os.makedirs(f"TOWest")
    if not os.path.exists(f"TOWest/list"):
        os.makedirs(f"TOWest/list")
    if not os.path.exists(f"TONorth"):
        os.makedirs(f"TONorth")
    if not os.path.exists(f"TONorth/list"):
        os.makedirs(f"TONorth/list")
    if not os.path.exists(f"TOSouth"):
        os.makedirs(f"TOSouth")
    if not os.path.exists(f"TOSouth/list"):
        os.makedirs(f"TOSouth/list")
    if not os.path.exists(f"AllTO"):
        os.makedirs(f"AllTO")
    if not os.path.exists(f"AllTO/list"):
        os.makedirs(f"AllTO/list")
    if not os.path.exists(f"files_mail"):
        os.makedirs(f"files_mail")

create_folder()


# Функция отправки сообщения в телеграмм
def send_telegram(text_to_bot):
    """
    Функция отправки сообщений в телеграм.
    Есть два варианта, отправка в чат и отправка в личку. Включается через конфиг.
    """
    print(f"Функция отправки сообщения в телеграмм. {text_to_bot}")
    url_msg = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    # Будем отправлять сообщение в чат
    if config.send_to_chat:
        data_to_chat = {
            'chat_id': config.chat_id,
            'text': text_to_bot,
            'parse_mode': 'HTML'
        }
        requests.post(url=url_msg, data=data_to_chat)

    # Будем отправлять сообщение в личку
    if config.send_to_ls:
        data_to_user = {
            'chat_id': config.tg_user_id,
            'text': text_to_bot,
            'parse_mode': 'HTML'
        }
        requests.post(url=url_msg, data=data_to_user)


# Отдельная функция для отправки сообщений в личку.
def send_telegram_to_ls(text_to_bot):
    """
    Функция отправки сообщений в телеграм.
    Исключительно для отправки в личку.
    """
    print(f"Функция отправки сообщения в телеграмм. {text_to_bot}")
    url_msg = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'

    # Будем отправлять сообщение в личку
    data_to_user = {
        'chat_id': config.tg_user_id,
        'text': text_to_bot,
        'parse_mode': 'HTML'
    }
    requests.post(url=url_msg, data=data_to_user)


# Функция отправки файла в телеграмм
def send_telegram_file(file_name):
    """
    Функция отправки файлов в телеграм.
    Есть два варианта, отправка в чат и отправка в личку. Включается через конфиг.
    """
    print(f"Функция отправки файла в телеграмм.")
    url_file = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendDocument'

    data_for_file = {
        'chat_id': config.chat_id,
        # 'caption': "Отчёт"
    }
    data_for_file_ls = {
        'chat_id': config.tg_user_id,
        # 'caption': "Отчёт"
    }
    # Отправка файла в общий чат
    if config.send_to_chat:
        with open(file_name, 'rb') as f:
            files = {'document': f}
            requests.post(url_file, data=data_for_file, files=files)
            # requests.post(url_file, data=data_for_file_ls, files=files)

    # # Отправка файла в личку
    if config.send_to_ls:
        with open(file_name, 'rb') as f:
            files = {'document': f}
            # requests.post(url_file, data=data_for_file, files=files)
            requests.post(url_file, data=data_for_file_ls, files=files)


def start():
    """
    Основная функция запускающая все парсеры /n
    1. Получение даты. Настройки берем из конфига.
    2. Парсер Юзера, одна ссылка на все ТО за день.
    3. Парсер почты. Проверка почты на новое сообение
    4. Парсер выгрузки с почты для ЭтХоума.
    5. Отправка в ексель для сохранения по ТО + общий файл для поиска потеряшек.
    6. Отправка файлов в чат/личку телеграмма.
    7. Составление и отправка списка домов для учета количества подключений.
    """
    # 1. Получение даты. Настройки берем из конфига.
    # Дату запуска соберем тут.
    # Получим дату и рассчитаем на -1 день(или как в конфиге), то есть за "вчера".
    date_now = datetime.now()
    start_day = date_now - timedelta(config.days_ago)  # здесь мы выставляем минус день
    date = start_day.strftime("%d.%m.%Y")

    # 2. Парсер Юзера, одна ссылка на все ТО за день.
    # parser_userside.get_token()  # Обновим токен
    et = []
    et = parser_userside.get_html(date)

    # 3. Парсер почты. Проверка почты на новое сообщение
    parser_mail.start_module()  # Обновим настройки почты
    parser_mail.check_mail()
    # Сделаем задержку для проверки и сохранения писем с почты.
    time.sleep(config.delay_mail)

    # 4. Парсер выгрузки с почты для ЭтХоума.
    houm = []
    houm = parser_mail.start(date)

    print(f"et {et}")
    print(f"houm {houm}")
    lst_to_exel = et + houm
    print(lst_to_exel)

    # 5. Отправка в ексель для сохранения по ТО + общий файл для поиска потеряшек.
    count_dict = to_exel.save_to_exel(lst_to_exel, date)
    to_exel.save_to_exel(lst_to_exel, date)
    to_exel.save_to_exel(lst_to_exel, date, "TONorth")
    to_exel.save_to_exel(lst_to_exel, date, "TOSouth")
    to_exel.save_to_exel(lst_to_exel, date, "TOWest")
    to_exel.save_to_exel(lst_to_exel, date, "TOEast")

    # 6. Отправка файлов в чат/личку телеграмма.
    send_telegram(f"Отчет за {date}")
    send_telegram_file(f"TONorth/TONorth_{date}.xls")
    send_telegram_file(f"TOSouth/TOSouth_{date}.xls")
    send_telegram_file(f"TOWest/TOWest_{date}.xls")
    send_telegram_file(f"TOEast/TOEast_{date}.xls")
    send_telegram_file(f"AllTO/AllTO_{date}.xls")

    # 7. Составление и отправка списка домов для учета количества подключений.
    # Больше не актуально. == Запускаю по просьбе Игоря
    count_dict_text = ""
    for k, v in count_dict.items():
        count_dict_text += f"{k}: {v} \n"

    # send_telegram_to_ls(f"Счетчик домов за {date}")
    send_telegram(f"Счетчик домов за {date}")
    # send_telegram_to_ls(count_dict_text)
    send_telegram(count_dict_text)


def main():
    # В случае теста сразу запустим создание отчета
    if config.global_test_day:
        start()
    # Автоматический запуск парсера по таймеру.
    # Время запуска берется из конфига(строка)
    schedule.every().day.at(config.time_for_start_parser).do(start)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
