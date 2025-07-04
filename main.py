
import os
import time
import asyncio
import logging
from datetime import datetime, timedelta

import requests
import schedule
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import config
import to_exel
import parser_mail
import parser_userside

# Настройка логирования
logging.basicConfig(level=logging.INFO)

logging.debug("Это отладочное сообщение")
logging.info("Это информационное сообщение")
logging.warning("Это предупреждение")
logging.error("Это ошибка")
logging.critical("Это критическая ошибка")

logger = logging.getLogger(__name__)

# Устанавливаем уровень логирования из конфига
log_level = getattr(logging, config.main_logger.upper(), logging.INFO)
logger.setLevel(log_level)

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
    logger.debug(f"Функция отправки сообщения в телеграмм. {text_to_bot}")
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
    logger.debug(f"Функция отправки сообщения в телеграмм. {text_to_bot}")
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
    logger.debug(f"Функция отправки файла в телеграмм.")
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


async def start():
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
    # et = parser_userside.get_html(date)

    # 3. Парсер почты. Проверка почты на новое сообщение
    parser_mail.start_module()  # Обновим настройки почты
    parser_mail.check_mail()
    # Сделаем задержку для проверки и сохранения писем с почты.
    time.sleep(config.delay_mail)

    # 4. Парсер выгрузки с почты для ЭтХоума.
    houm = []
    houm = parser_mail.start(date)

    logger.debug(f"et {et}")
    logger.debug(f"houm {houm}")
    lst_to_exel = et + houm
    logger.debug(lst_to_exel)

    # 5. Отправка в ексель для сохранения по ТО + общий файл для поиска потеряшек.
    count_dict_1, count_dict_2 = to_exel.save_to_exel(lst_to_exel, date)
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
    # Сделал два списка.
    # TODO переделать под любое количество списков, принимая массив с массивами
    send_telegram(f"Счетчик домов за {date}")

    count_dict_text_1 = ""
    for k, v in count_dict_1.items():
        count_dict_text_1 += f"{k}: {v} \n"
    # send_telegram_to_ls(f"Счетчик домов за {date}")
    # send_telegram_to_ls(count_dict_text)
    send_telegram(count_dict_text_1)

    count_dict_text_2 = ""
    for k, v in count_dict_2.items():
        count_dict_text_2 += f"{k}: {v} \n"
    # send_telegram_to_ls(f"Счетчик домов за {date}")
    # send_telegram_to_ls(count_dict_text)
    send_telegram(count_dict_text_2)



# Функция для запуска по таймеру
async def start_scheduled_morning():
    schedule.every().day.at(config.time_for_start_parser).do(
        lambda: asyncio.create_task(start()))

# Запуск расписания
async def run_scheduler():
    while True:
        schedule.run_pending()
        logger.info('Ожидание расписания')
        await asyncio.sleep(10)

async def main():
    # В случае теста сразу запустим создание отчета
    if config.global_test_day:
        await start()
    # Автоматический запуск парсера по таймеру.
    # Время запуска берется из конфига(строка)
    #
    # schedule.every().day.at(config.time_for_start_parser).do(
    #     lambda: asyncio.create_task(start()))

    # Удаляем вебхук, если он был установлен
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск утреннего расписания
    await start_scheduled_morning()

    # Запуск шедулера в фоновом режиме
    asyncio.create_task(run_scheduler())

    # Запускаем поллинг
    logger.info("Бот запущен")
    await dp.start_polling(bot)

  #schedule.every().day.at(config.time_for_start_parser).do(start)
    # while True:
        # logger.debug("Ожидаем работы расписания.")
       # schedule.run_pending()
       # time.sleep(config.main_sleep)



if __name__ == "__main__":
    asyncio.run(main())
