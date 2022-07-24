import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

token = os.getenv("BOT_TOKEN")
storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(
    bot=bot,
    storage=storage
)
