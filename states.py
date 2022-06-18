from aiogram.dispatcher.filters.state import StatesGroup, State


class Bank(StatesGroup):
    start = State()
    device = State()


class TinkoffForm(StatesGroup):
    start = State()
    wait_name = State()
    wait_phone_num = State()
    wait_start_sum = State()
    wait_transfer_sum = State()


class SberbankForm(StatesGroup):
    start = State()
    wait_name = State()
    wait_transfer_sum = State()
