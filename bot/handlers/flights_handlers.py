from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from bot.states.flights_states import FlightsStates
from bot.filters.blacklist import BlacklistFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from bot.db.models import Courier
from bot.keyboards.start import get_to_start_kb
from bot.keyboards.inline import del_flight, DelFlight
from datetime import datetime

router = Router()

@router.message(Text(text="📋 Мои перелеты", ignore_case=True), BlacklistFilter())
async def my_flights(message: Message, state: FSMContext, session: AsyncSession):
    """
    Хэндлер для получения списка перелетов пользователя по user_id
    :param message:
    :param state:
    :param session:
    :return:
    """
    await state.set_state(FlightsStates.flights)
    today = datetime.today()
    user_id = message.from_user.id
    query = (await session.scalars(select(Courier)
                                   .where(Courier.user_id == user_id)
                                   .where(Courier.flight_date >= today)
                                   .where(Courier.status == True))).all()
    await message.answer('Вот что мне удалось найти:', reply_markup=get_to_start_kb())
    for flight in query:
        await message.answer(f'<b>Дата: {flight.flight_date.strftime("%d.%m.%Y")}</b>\n'
                             f'Имя: <a href="tg://user?id={flight.user_id}">{flight.user_name}</a>\n'
                             f'Контакт: {flight.phone}\n'
                             f'Примечание: {flight.info}', reply_markup=del_flight(flight.id)
                             )

@router.callback_query(DelFlight.filter(F.action == "delete"))
async def send_random_value(callback: CallbackQuery, callback_data: DelFlight, session: AsyncSession):
    """
    Хэндлер для удаления перелета курьера
    :param callback:
    :param callback_data:
    :param session:
    :return:
    """
    flight_id = callback_data.flight_id
    await session.execute(update(Courier).where(Courier.id == flight_id).values(status=False))
    await session.commit()
    await callback.message.delete()
    await callback.answer(
        text="Перелет удален из базы!",
        show_alert=True
    )

