from aiogram import executor

from bot import dp
from startup import on_startup

executor.start_polling(
    dispatcher=dp,
    skip_updates=True,
    on_startup=on_startup
)
