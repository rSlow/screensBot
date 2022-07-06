
from aiogram import types
from aiogram.dispatcher import FSMContext, filters

import settings
from bot import dp
from functions import validators, send_files
from functions.main import get_render_func
from keyboards.main import CancelKeyboard, RandomSumKeyboard
from states import TinkoffForm


@dp.message_handler(filters.Text(equals=settings.banks["Тинькофф"]["on_banks"]),
                    state=settings.banks["Тинькофф"]["state"].start)
async def tinkoff_form_name(message: types.Message, state: FSMContext):
    await TinkoffForm.next()

    async with state.proxy() as proxy:
        proxy["on_bank"] = message.text
        proxy["args"] = {}

    await message.answer(
        text="Введите имя получателя:",
    )
    await message.answer(
        text="Поддерживаемый формат:\n"
             "Валерия Д.\n"
             "Валерия Демченко",
        reply_markup=CancelKeyboard()
    )


@dp.message_handler(state=TinkoffForm.wait_name)
async def tinkoff_form_phone_num(message: types.Message, state: FSMContext):
    name = validators.validate_name(name=message.text)
    if name is not False:
        await TinkoffForm.next()

        async with state.proxy() as proxy:
            proxy["args"]["name"] = name

        await message.answer(
            text="Введите номер телефона:",
            reply_markup=CancelKeyboard()
        )
    else:
        await message.answer(
            text="Неправильный формат имени. Попробуйте еще раз...",
            reply_markup=CancelKeyboard()
        )


@dp.message_handler(state=TinkoffForm.wait_phone_num)
async def tinkoff_form_start_sum(message: types.Message, state: FSMContext):
    phone_num = validators.validate_phone_num(phone_num=message.text)
    if phone_num is not False:
        await TinkoffForm.next()

        async with state.proxy() as proxy:
            proxy["args"]["phone_num"] = phone_num

        await message.answer(
            text="Введите начальную сумму (до перевода):\n"
                 "Либо нажми кнопку, чтобы подставить любое случайное значение от 10 до 50 тысяч",
            reply_markup=RandomSumKeyboard()
        )

    else:
        await message.answer(
            text="Неправильный формат номера. Попробуйте еще раз...",
            reply_markup=CancelKeyboard()
        )


@dp.message_handler(state=TinkoffForm.wait_start_sum)
async def tinkoff_form_start_sum(message: types.Message, state: FSMContext):
    start_sum = validators.validate_sum(message.text)
    if start_sum is not False and start_sum > 0:
        await TinkoffForm.next()

        async with state.proxy() as proxy:
            proxy["args"]["start_sum"] = start_sum

        await message.answer(
            text="Введите сумму перевода:",
            reply_markup=CancelKeyboard()
        )
    else:
        await message.answer(
            text="Неправильная форма суммы. Попробуйте еще раз...",
            reply_markup=CancelKeyboard()
        )


@dp.message_handler(state=TinkoffForm.wait_transfer_sum)
async def tinkoff_send_file(message: types.Message, state: FSMContext):
    transfer_sum = validators.validate_sum(message.text)
    async with state.proxy() as proxy:
        start_sum = proxy["args"]["start_sum"]

    if transfer_sum is not False and start_sum >= transfer_sum > 0:
        async with state.proxy() as proxy:
            name = proxy["args"]["name"]
            phone_num = proxy["args"]["phone_num"]
            start_sum = proxy["args"]["start_sum"]

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
            phone_num=phone_num,
            start_sum=start_sum,
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
