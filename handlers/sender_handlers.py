from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Courier, Stats, Stats_search
from filters.blacklist import BlacklistFilter
from states.sender_states import SenderStates
from utils.misc.validators import isvalid_name, isvalid_city, isvalid_info
from keyboards.citypicker import get_country_keyboard, city_keyboard, cities_by_country
from keyboards.start import get_to_search_kb
from datetime import datetime

router = Router()

@router.message(Text(text="Новый поиск", ignore_case=True), BlacklistFilter())
@router.message(Text(text="📦 Хочу отправить", ignore_case=True), BlacklistFilter())
async def answer_yes(message: Message, state: FSMContext):
    await message.answer("Выберите откуда вы хотите отправить посылку.",reply_markup=get_country_keyboard())
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
    if city != "Назад":
        if isvalid_city(city):
            await state.update_data(city_from=city)
            await message.answer('Выберите в какую страну хотите отправить посылку.', reply_markup=get_country_keyboard())
            await state.set_state(SenderStates.waiting_for_country_to)
        else:
            await message.answer('Неправильный формат, используйте только русские или латинские буквы.')
    else:
        await state.set_state(SenderStates.waiting_for_country_from)
        await message.answer("Выберите откуда вы хотите отправить посылку.",reply_markup=get_country_keyboard())

@router.message(SenderStates.waiting_for_country_to)
async def country_to(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите в какой город вы хотите отправить посылку.',
                             reply_markup=city_keyboard(country))
        await state.set_state(SenderStates.waiting_for_city_to)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(SenderStates.waiting_for_city_to)
async def city_to(message: Message, state: FSMContext, session: AsyncSession):
    city = message.text.strip()
    if city != "Назад":
        data = await state.get_data()
        if city != data['city_from']:
            if isvalid_city(city):
                await state.update_data(city_to=city)
                data = await state.get_data()
                today = datetime.today()
                query = (await session.scalars(select(Courier)
                                               .where(Courier.city_from == data['city_from'])
                                               .where(Courier.city_to == data['city_to'])
                                               .where(Courier.flight_date >= today).where(Courier.status == True)
                                               .order_by(Courier.flight_date))).all()
                if query:
                    await message.answer('Вот что мне удалось найти:')
                    for courier in query:
                        await message.answer(f'<b>Дата: {courier.flight_date.strftime("%d.%m.%Y")}</b>\n'
                                             f'Имя: <a href="tg://user?id={courier.user_id}">{courier.user_name}</a>\n'
                                             f'Контакт: {courier.phone}\n'
                                             f'Примечание: {courier.info}',
                                             reply_markup=get_to_search_kb())
                else:
                    await message.answer('Ничего не найдено :(', reply_markup=get_to_search_kb())
                await session.commit()
            await state.clear()
        else:
            await message.answer('Города отправления и назначения должны различаться.')
    else:
        await state.set_state(SenderStates.waiting_for_country_to)
        await message.answer("Выберите куда вы хотите отправить посылку.", reply_markup=get_country_keyboard())