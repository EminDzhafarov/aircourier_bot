from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

def send_msg(phone):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text='Написать курьеру',
        url=f'https://t.me/{(phone.translate({ord(i): None for i in ["-", " "]}))}')
    )
    return builder.as_markup()

class DelFlight(CallbackData, prefix="my"):
    action: str
    flight_id: int

def del_flight(flight_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text='Удалить',
        callback_data=DelFlight(action="delete", flight_id=flight_id).pack(),
    ))
    return builder.as_markup()