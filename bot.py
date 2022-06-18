import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

token = os.getenv("TOKEN")  # 5394261479:AAE_SnM4TrEUbF3Xczus7vK_mWWgFU-hXls
storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(
    bot=bot,
    storage=storage
)
