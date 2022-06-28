from aiogram import types
from random import randint

import settings


class CancelKeyboard(types.ReplyKeyboardMarkup):
    def __init__(self):
        super(CancelKeyboard, self).__init__(
            resize_keyboard=True,
            one_time_keyboard=True
        )
        self.add("На главную")


class RandomSumKeyboard(types.ReplyKeyboardMarkup):
    def __init__(self):
        super(RandomSumKeyboard, self).__init__(
            resize_keyboard=True,
            one_time_keyboard=True
        )
        value = randint(1000000, 5000000) / 100
        self.add(f"{value:.2f}")
        self.add("На главную")


class DeviceKeyboard(types.ReplyKeyboardMarkup):
    devices = list(settings.DEVICES)

    def __init__(self):
        super(DeviceKeyboard, self).__init__(resize_keyboard=True)
        self.add(*self.devices)
        # self.add("Тест")
        # self.add("На главную")


class BanksKeyboard(types.ReplyKeyboardMarkup):
    banks = list(settings.banks)

    def __init__(self):
        super(BanksKeyboard, self).__init__(resize_keyboard=True)
        self.add(*self.banks)
        self.add("На главную")


class OnBankKeyboard(types.ReplyKeyboardMarkup):
    def __init__(self, bank: str):
        super(OnBankKeyboard, self).__init__(resize_keyboard=True)
        on_banks = settings.banks[bank]["on_banks"]
        self.add(*on_banks)
        self.add("На главную")
