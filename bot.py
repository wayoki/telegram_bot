import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import cancelling, creating
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage())

async def main():
    dp.include_router(cancelling.router)
    dp.include_router(creating.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
