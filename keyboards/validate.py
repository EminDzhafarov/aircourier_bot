from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_valid_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Все правильно")
    kb.button(text="Начать заново")
    kb.button(text="В начало")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)