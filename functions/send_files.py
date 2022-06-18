import logging
from datetime import datetime

from aiogram import types
from io import BytesIO
from keyboards.main import CancelKeyboard


async def send_file(message: types.Message,
                    image_io: BytesIO,
                    bank,
                    on_bank,
                    device):

    photo = types.InputFile(
        path_or_bytesio=image_io,
        filename=f"{datetime.now():%d_%m_%y__%H_%M_%S}.PNG"
    )

    await message.answer_document(
        document=photo,
        reply_markup=CancelKeyboard()
    )

    logging.info(f"[SCREEN] {bank}->{on_bank}/{device}")
