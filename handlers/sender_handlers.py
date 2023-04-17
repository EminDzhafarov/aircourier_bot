from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Text(text="📦 Хочу отправить", ignore_case=True))
async def answer_yes(message: Message):
    await message.answer(
        "Это отлично!",
        reply_markup=ReplyKeyboardRemove()
    )