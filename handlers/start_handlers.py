from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.types import Message
from keyboards.start import get_start_kb
from filters.blacklist import BlacklistFilter

router = Router()

# Хэндлер на команду /start
@router.message(Command("start"), BlacklistFilter())
async def cmd_start(message: Message) -> None:
        await message.answer("Привет! Этот бот поможет найти попутчиков для доставки посылок самолетом.\n\n"\
                "<i>Отправляя сообщение, вы соглашаетесь на обработку персональных данных.</i>\n\n"\
                "Для начала выберите"\
                             " что вы хотите сделать.", reply_markup=get_start_kb())

@router.message(Text(text="В начало", ignore_case=True), BlacklistFilter())
async def begining(message: Message) -> None:
        await message.answer("Выберите что вы хотите сделать.", reply_markup=get_start_kb())