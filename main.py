import asyncio
import time
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests

import config
from parser_mail import start

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

def main(date):
    import parser_userside
    # date = "17.09.2024"
    et = []
    et = parser_userside.get_html(date)
    # et = parser_userside.get_html("14.09.2024")
    # parser_userside.get_html("15.09.2024")
    # parser_userside.get_html("16.09.2024")
    # parser_userside.get_html("17.09.2024")
    # parser_userside.get_html("18.09.2024")
    # parser_userside.get_html("19.09.2024")
    # parser_userside.get_html("20.09.2024")
    import parser_mail
    parser_mail.check_mail()

    houm = []
    houm = parser_mail.start(date)

    print(f"et {et}")
    print(f"houm {houm}")
    lst_to_exel = et + houm
    print(lst_to_exel)

    import to_exel
    to_exel.save_to_exel(lst_to_exel, date)
    # to_exel.save_to_exel(lst_to_exel, date, "TONorth")
    # to_exel.save_to_exel(lst_to_exel, date, "TOSouth")
    # to_exel.save_to_exel(lst_to_exel, date, "TOWest")
    # to_exel.save_to_exel(lst_to_exel, date, "TOEast")

    # await dp.start_polling(bot)
    # start_parser()
    # while True:
    #     time.sleep(config.delay)
        # start_parser()


if __name__ == "__main__":
    main("16.09.2024")
    # main("17.09.2024")
    # main("18.09.2024")
    # main("19.09.2024")
    # main("20.09.2024")
    # main("21.09.2024")
    # asyncio.run(main())
    # parser.get_html("west")
