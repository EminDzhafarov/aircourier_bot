from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.start import get_start_kb
from filters.blacklist import BlacklistFilter
from filters.flights import FlightsFilter
from states.start_states import StartStates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Stats
from datetime import datetime

router = Router()

# Хэндлер на команду /start
@router.message(Command("start"), BlacklistFilter(), FlightsFilter())
async def cmd_start(message: Message, flights: bool, state: FSMContext, session: AsyncSession) -> None:
        stats_query = await session.execute(select(Stats).where(Stats.user_id == message.from_user.id))
        if not stats_query.scalar():
                await session.merge(Stats(user_id=message.from_user.id, timestamp=datetime.now()))
        await session.commit()
        await state.set_state(StartStates.start)
        await message.answer("Привет! Этот бот поможет найти попутчиков для доставки посылок самолетом.\n\n"\
                "<i>Отправляя сообщение, вы соглашаетесь на обработку персональных данных.</i>\n\n"\
                "Для начала выберите"\
                             " что вы хотите сделать.", reply_markup=get_start_kb(flights))

# Хэндлер на текст "В начало"
@router.message(Text(text="В начало", ignore_case=True), BlacklistFilter(), FlightsFilter())
async def begining(message: Message, flights: bool, state: FSMContext) -> None:
        await state.set_state(StartStates.start)
        await message.answer("Выберите что вы хотите сделать.", reply_markup=get_start_kb(flights))