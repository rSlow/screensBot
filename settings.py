import states
from functions import render

DEVICES = [
    "Android",
    "iPhone"
]


def get_on_bank_kw(*functions):
    if len(functions) == 1:
        raise ValueError
    return dict(list(zip(DEVICES, functions)))


banks = {
    "Сбербанк": {
        "on_banks": {
            "На Сбербанк": get_on_bank_kw(
                render.android.sberbank.sberbank_sberbank_phone_android,
                render.iphone.sberbank.sberbank_sberbank_phone_iphone
            ),
        },
        "state": states.SberbankForm,
    },
    "Тинькофф": {
        "on_banks": {
            # "На Сбербанк": get_on_bank_kw(
            #
            # ),
            "На Тинькофф": get_on_bank_kw(
                render.android.tinkoff.tinkoff_tinkoff_phone_android,
                render.iphone.tinkoff.tinkoff_tinkoff_phone_iphone
            ),
        },
        "state": states.TinkoffForm,
    },
}
