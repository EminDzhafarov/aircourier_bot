from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_admin_start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить")
    kb.button(text="Удалить")
    kb.button(text="Добавить рейс")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


def get_admin_add() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Подтверждаю добавление")
    kb.button(text="В начало")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_admin_del() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Подтверждаю удаление")
    kb.button(text="В начало")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
