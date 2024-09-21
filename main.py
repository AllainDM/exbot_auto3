import asyncio
import time
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests

import config


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

create_folder()

def main():
    import parser_userside
    # parser.get_html("13.09.2024")
    parser_userside.get_html("14.09.2024")
    parser_userside.get_html("15.09.2024")
    parser_userside.get_html("16.09.2024")
    parser_userside.get_html("17.09.2024")
    parser_userside.get_html("18.09.2024")
    parser_userside.get_html("19.09.2024")
    parser_userside.get_html("20.09.2024")
    # await dp.start_polling(bot)
    # start_parser()
    # while True:
    #     time.sleep(config.delay)
        # start_parser()


if __name__ == "__main__":
    main()
    # asyncio.run(main())
    # parser.get_html("west")
