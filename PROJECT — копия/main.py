import asyncio
from aiogram import Bot, Dispatcher, types
from handlers import register_routes
from dotenv import load_dotenv

import os

load_dotenv()

async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    register_routes(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен!')