from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import find_couriers, add_search_stat
from filters.blacklist import BlacklistFilter
from states.sender_states import SenderStates
from utils.misc.validators import isvalid_city
from keyboards.citypicker import get_country_keyboard, city_keyboard, cities_by_country
from keyboards.start import get_to_search_kb
from keyboards.inline import send_msg

router = Router()


@router.message(Text(text="Новый поиск", ignore_case=True), BlacklistFilter())
@router.message(Text(text="📦 Хочу отправить", ignore_case=True), BlacklistFilter())
async def answer_yes(message: Message, state: FSMContext):
    """
    Хэндлер для запроса страны вылета курьера
    :param message:
    :param state:
    :return:
    """
    await message.answer("Выберите откуда вы хотите отправить посылку.", reply_markup=get_country_keyboard())
    await state.set_state(SenderStates.waiting_for_country_from)


@router.message(SenderStates.waiting_for_country_from)
async def country_from(message: Message, state: FSMContext):
    """
    Хэндлер для запроса города вылета курьера
    :param message:
    :param state:
    :return:
    """
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите из какого города вы хотите отправить посылку.',
                             reply_markup=city_keyboard(country))
        await state.set_state(SenderStates.waiting_for_city_from)
    else:
        await message.answer('Сервис пока не работает в этой стране.')


@router.message(SenderStates.waiting_for_city_from)
async def city_from(message: Message, state: FSMContext):
    """
    Хэндлер для запроса страны прилета курьера
    :param message:
    :param state:
    :return:
    """
    city = message.text.strip()
    if city != "Назад":
        if isvalid_city(city):
            await state.update_data(user_id=message.from_user.id, city_from=city)
            await message.answer('Выберите в какую страну хотите отправить посылку.',
                                 reply_markup=get_country_keyboard())
            await state.set_state(SenderStates.waiting_for_country_to)
        else:
            await message.answer('Неправильный формат, используйте только русские или латинские буквы.')
    else:
        await state.set_state(SenderStates.waiting_for_country_from)
        await message.answer("Выберите откуда вы хотите отправить посылку.", reply_markup=get_country_keyboard())


@router.message(SenderStates.waiting_for_country_to)
async def country_to(message: Message, state: FSMContext):
    """
    Хэндлер для получения города прилета курьера
    :param message:
    :param state:
    :return:
    """
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите в какой город вы хотите отправить посылку.',
                             reply_markup=city_keyboard(country))
        await state.set_state(SenderStates.waiting_for_city_to)
    else:
        await message.answer('Сервис пока не работает в этой стране.')


@router.message(SenderStates.waiting_for_city_to)
async def city_to(message: Message, state: FSMContext, session: AsyncSession):
    """
    Хэндлер для поиска курьера по полученным данным из хранилища
    :param message:
    :param state:
    :param session:
    :return:
    """
    city = message.text.strip()
    if city != "Назад":
        data = await state.get_data()
        if city != data['city_from']:
            if isvalid_city(city):
                await state.update_data(city_to=city)
                data = await state.get_data()
                await add_search_stat(session, data)
                couriers = await find_couriers(session, data)
                if couriers:
                    await message.answer('Вот что мне удалось найти:', reply_markup=get_to_search_kb())
                    for courier in couriers:
                        await message.answer(f'<b>Дата: {courier.flight_date.strftime("%d.%m.%Y")}</b>\n'
                                             f'<b>Имя:</b> <a href="tg://user?id={courier.user_id}">'
                                             f'{courier.user_name}</a>\n'
                                             f'<b>Контакт:</b> {courier.phone}\n'
                                             f'<b>Примечание:</b> {courier.info}',
                                             reply_markup=send_msg(courier.phone))
                    await message.answer("Обратите внимание: некоторые курьеры запрещают писать себе настройками "
                                         "приватности, но вы можете добавить их в контакты по номеру телефона "
                                         "или позвонить.")
                else:
                    await message.answer('Ничего не найдено :(', reply_markup=get_to_search_kb())
            await state.clear()
        else:
            await message.answer('Города отправления и назначения должны различаться.')
    else:
        await state.set_state(SenderStates.waiting_for_country_to)
        await message.answer("Выберите куда вы хотите отправить посылку.", reply_markup=get_country_keyboard())
