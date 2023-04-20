from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Courier, Stats, Stats_search
from states.sender_states import SenderStates
from utils.misc.validators import isvalid_name, isvalid_city, isvalid_info
from keyboards.citypicker import get_country_keyboard, city_keyboard, cities_by_country
from datetime import datetime

router = Router()

@router.message(Text(text="📦 Хочу отправить", ignore_case=True))
async def answer_yes(message: Message, state: FSMContext):
    await message.answer(
        "Выберите откуда вы хотите отправить посылку.",
        reply_markup=get_country_keyboard()
    )
    await state.set_state(SenderStates.waiting_for_country_from)

@router.message(SenderStates.waiting_for_country_from)
async def country_from(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите из какого города вы хотите отправить посылку.',
                             reply_markup=city_keyboard(country))
        await state.set_state(SenderStates.waiting_for_city_from)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(SenderStates.waiting_for_city_from)
async def city_from(message: Message, state: FSMContext):
    city = message.text.strip()
    if isvalid_city(city):
        await state.update_data(city_from=city)
        await message.answer('Выберите в какую страну хотите отправить посылку.', reply_markup=get_country_keyboard())
        await state.set_state(SenderStates.waiting_for_country_to)
    else:
        await message.answer('Неправильный формат, используйте только русские или латинские буквы.')

@router.message(SenderStates.waiting_for_country_to)
async def country_to(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите в какой город вы хотите отправить посылку.', \
                             reply_markup=city_keyboard(country))
        await state.set_state(SenderStates.waiting_for_city_to)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(SenderStates.waiting_for_city_to)
async def city_to(message: Message, state: FSMContext, session: AsyncSession):
    city = message.text.strip()
    data = await state.get_data()
    if city != data['city_from']:
        if isvalid_city(city):
            await state.update_data(city_to=city)
            data = await state.get_data()
            today = datetime.today()
            query = (await session.execute(select(Courier).where(Courier.city == data['city_from']).where(Courier.dest == data['city_to']) \
                    .where(Courier.flight_date >= today).where(Courier.status == True) \
                    .order_by(Courier.flight_date))).all()
            if query:
                await message.answer('Вот что мне удалось найти:', \
                                     reply_markup=ReplyKeyboardRemove())
                for courier in query:
                    await message.answer(f'<b>Дата: {courier.flight_date.strftime("%d.%m.%Y")}</b>\n'
                                         f'Имя: <a href="tg://user?id={courier.user_id}">{courier.user_name}</a>\n' \
                                         f'Контакт: {courier.phone}\n' \
                                         f'Примечание: {courier.extra}', \
                                         parse_mode='HTML')
            else:
                await message.answer('Ничего не найдено :(')
            await session.commit()
        await state.clear()