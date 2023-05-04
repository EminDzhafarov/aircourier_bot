from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="✈️ Хочу доставить")
    kb.button(text="📦 Хочу отправить")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_to_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="В начало")
    return kb.as_markup(resize_keyboard=True)

def get_to_search_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="В начало")
    kb.button(text="Новый поиск")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)