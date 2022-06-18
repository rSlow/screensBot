from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from functions.render import settings
from functions.main import grade
from aiogram.types import Message


async def sberbank_sberbank_phone_android(
        name,
        transfer_sum,
        message: Message
):
    str_transfer_sum = f"{transfer_sum}".replace(".", ",")

    image_io = BytesIO()
    image = Image.open(
        fp=settings.template_sberbank_android
    )
    draw = ImageDraw.Draw(image)

    # Имя
    draw.text(
        xy=(540, 780),
        text=f"{name}",
        font=ImageFont.truetype(
            font=settings.font_android,
            size=44
        ),
        anchor="mm"
    )

    # Сумма перевода
    draw.text(
        xy=(540, 660),
        text=f"{grade(str_transfer_sum)} ₽",
        font=ImageFont.truetype(
            font=settings.font_android,
            size=84
        ),
        anchor="mm"
    )

    # Время
    draw.text(
        xy=(45, 35),
        text=f"{message.date:%H:%M}",
        font=ImageFont.truetype(
            font=settings.font_android,
            size=32,
        )
    )

    image.save(image_io, "PNG")
    image_io.seek(0)

    return image_io
