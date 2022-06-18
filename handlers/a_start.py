from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

import settings
from bot import dp
from functions import send_files
from functions.main import get_render_func
from keyboards.main import BanksKeyboard, OnBankKeyboard, DeviceKeyboard
from states import Bank


@dp.message_handler(filters.Text(equals="На главную"), state="*")
@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()

    await Bank.start.set()

    await message.answer(
        text="Добро пожаловать. Выберите тип устройства:",
        reply_markup=DeviceKeyboard()
    )


@dp.message_handler(filters.Text(equals=settings.DEVICES), state=Bank.start)
async def choose_device(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy["device"] = message.text

    await Bank.device.set()

    await message.answer(
        text="Выберите банк для перевода:",
        reply_markup=BanksKeyboard()
    )


@dp.message_handler(filters.Text(equals=list(settings.banks)), state=Bank.device)
async def bank_menu(message: types.Message, state: FSMContext):
    bank = message.text
    bank_state = settings.banks[bank]["state"]
    await bank_state.first()

    keyboard = OnBankKeyboard(bank=bank)

    async with state.proxy() as proxy:
        proxy["bank"] = bank

    await message.answer(
        text="Куда переводим?",
        reply_markup=keyboard
    )


# @dp.message_handler(filters.Text(equals="Тест"), state=Bank.start)
async def test(message: types.Message):
    bank = "Тинькофф"
    on_bank = "На Тинькофф"
    device = "iPhone"

    render_func = get_render_func(
        bank=bank,
        on_bank=on_bank,
        device=device
    )

    image_io = await render_func(
        name="Евгений П.",
        phone_num="+7 (914) 665-64-93",
        start_sum=25434.56,
        transfer_sum=250
    )

    await send_files.send_file(
        image_io=image_io,
        message=message,
        bank=bank,
        on_bank=on_bank,
        device=device
    )
