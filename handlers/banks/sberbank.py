from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from functions.main import get_render_func
import settings
from bot import dp
from functions import validators, send_files
from keyboards.main import CancelKeyboard
from states import SberbankForm


@dp.message_handler(filters.Text(equals=settings.banks["Сбербанк"]["on_banks"]),
                    state=settings.banks["Сбербанк"]["state"].start)
async def sberbank_form_name(message: types.Message, state: FSMContext):
    await SberbankForm.next()

    async with state.proxy() as proxy:
        proxy["on_bank"] = message.text
        proxy["args"] = {}

    await message.answer(
        text="Введите имя:",
    )
    await message.answer(
        text="Поддерживаемый формат:\n"
             "Валерия Владимировна Д.\n"
             "Валерия Владимировна Демченко",
        reply_markup=CancelKeyboard()
    )


@dp.message_handler(state=SberbankForm.wait_name)
async def sberbank_form_transfer_sum(message: types.Message, state: FSMContext):
    name = validators.validate_name(message.text)
    if name is not False:
        await SberbankForm.next()

        async with state.proxy() as proxy:
            proxy["args"]["name"] = name

        await message.answer(
            text="Введите сумму перевода:",
            reply_markup=CancelKeyboard()
        )
    else:
        await message.answer(
            text="Неправильный формат имени. Попробуйте еще раз...",
            reply_markup=CancelKeyboard()
        )


@dp.message_handler(state=SberbankForm.wait_transfer_sum)
async def sberbank_send_file(message: types.Message, state: FSMContext):
    transfer_sum = validators.validate_sum(message.text)

    if transfer_sum is not False and transfer_sum > 0:
        async with state.proxy() as proxy:
            name = proxy["args"]["name"]
            device = proxy["device"]
            on_bank = proxy["on_bank"]
            bank = proxy["bank"]

        render_func = get_render_func(
            bank=bank,
            on_bank=on_bank,
            device=device
        )

        image_io = await render_func(
            name=name,
            transfer_sum=transfer_sum,
        )

        await send_files.send_file(
            image_io=image_io,
            message=message,
            bank=bank,
            on_bank=on_bank,
            device=device
        )

    else:
        await message.answer(
            text="Неправильная форма суммы. Попробуйте еще раз...",
            reply_markup=CancelKeyboard()
        )
