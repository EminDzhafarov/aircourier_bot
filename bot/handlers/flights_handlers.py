from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from db.crud import get_flights, del_from_flight
from states.flights_states import FlightsStates
from filters.blacklist import BlacklistFilter
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.start import get_to_start_kb
from keyboards.inline import del_flight, DelFlight

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
    user_id = message.from_user.id
    flights = await get_flights(session, user_id)
    await message.answer('Вот что мне удалось найти:', reply_markup=get_to_start_kb())
    for flight in flights:
        await message.answer(f'<b>Дата: {flight.flight_date.strftime("%d.%m.%Y")}</b>\n'
                             f"{flight.city_from} ✈ {flight.city_to}\n"
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
    await del_from_flight(session, flight_id)
    await callback.message.delete()
    await callback.answer(
        text="Перелет удален из базы!",
        show_alert=True
    )
