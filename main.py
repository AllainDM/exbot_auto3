import asyncio
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests

import config


# Объект бота
bot = Bot(token=config.BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()


def main():
    import parser
    parser.get_html("05.09.2024")
    # await dp.start_polling(bot)
    # start_parser()
    # while True:
    #     time.sleep(config.delay)
        # start_parser()


if __name__ == "__main__":
    main()
    # asyncio.run(main())
    # parser.get_html("west")
