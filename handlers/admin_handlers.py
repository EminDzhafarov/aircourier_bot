from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from keyboards.admin import get_admin_start, get_admin_add, get_admin_del
from keyboards.start import get_to_start_kb
from keyboards.inline import del_blacklist, DelBlacklist
from states.admin_states import AdminStates
from filters.admin import AdminFilter
from db.models import Blacklist, Courier
from utils.misc.validators import isvalid_name, isvalid_city, isvalid_info
from keyboards.validate import get_valid_kb
from keyboards.inline import to_bot
from keyboards.citypicker import get_country_keyboard, city_keyboard, cities_by_country
from keyboards.calendar.simple_calendar import SimpleCalendarCallback as simple_cal_callback, SimpleCalendar
from dateutil.parser import isoparse
import settings
import phonenumbers

router = Router()

@router.message(Command("admin"), AdminFilter())
async def blacklist_start(message: Message, state: FSMContext):
    await state.set_state(AdminStates.start)
    await message.answer("Что нужно сделать?", reply_markup=get_admin_start())

@router.message(Text("Добавить"), AdminFilter())
async def blacklist_add(message: Message, state: FSMContext):
    await state.set_state(AdminStates.add)
    await message.answer("Введите user_id", reply_markup=ReplyKeyboardRemove)

@router.message(AdminStates.add)
async def blacklist_add(message: Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    await state.set_state(AdminStates.add_validator)
    await message.answer(f"Подтвердите добавление {user_id} в черный список.", reply_markup=get_admin_add())

@router.message(Text("Подтверждаю добавление"), AdminFilter())
async def blacklist_add(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(insert(Blacklist).values(user_id=data['user_id']))
    await session.commit()
    await state.clear()
    await message.answer("Пользователь добавлен в черный список.", reply_markup=get_to_start_kb())

@router.message(Text("Удалить"), AdminFilter())
async def blacklist_add(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(AdminStates.delete)
    query = (await session.scalars(select(Blacklist))).all()
    await message.answer("Вот черный список:", reply_markup=get_to_start_kb())
    for users in query:
        await message.answer(f'<a href="tg://user?id={users.user_id}">{users.user_id}</a>',
                             reply_markup=del_blacklist(users.user_id))

@router.callback_query(DelBlacklist.filter(F.action == "delete"))
async def send_random_value(callback: CallbackQuery, callback_data: DelBlacklist, session: AsyncSession):
    user_id = callback_data.user_id
    await session.execute(delete(Blacklist).where(Blacklist.user_id == user_id))
    await session.commit()
    await callback.message.delete()
    await callback.answer(
        text="Пользователь удален из ЧС!",
        show_alert=True
    )

@router.message(Text(text="Добавить рейс", ignore_case=True), AdminFilter())
async def courier_start(message: Message, state: FSMContext):
    await message.answer('user_id', reply_markup=get_to_start_kb())
    await state.set_state(AdminStates.waiting_for_id)

@router.message(AdminStates.waiting_for_id)
async def courier_start(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text.strip())
    await message.answer(
        'Имя',
        reply_markup=get_to_start_kb()
    )
    await state.set_state(AdminStates.waiting_for_name)

@router.message(AdminStates.waiting_for_name)
async def courier_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if isvalid_name(name):
        await state.update_data(user_name=name)
        await message.answer(f' Страна откуда',
                             reply_markup=get_country_keyboard())
        await state.set_state(AdminStates.waiting_for_country_from)
    else:
        await message.answer('Неправильный формат, используйте только русские или латинские буквы.')

@router.message(AdminStates.waiting_for_country_from)
async def country_from(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Город откуда',
                             reply_markup=city_keyboard(country))
        await state.set_state(AdminStates.waiting_for_city_from)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(AdminStates.waiting_for_city_from)
async def city_from(message: Message, state: FSMContext):
    city = message.text.strip()
    if city != "Назад":
        if isvalid_city(city):
            await state.update_data(city_from=city)
            await message.answer('Страна куда', reply_markup=get_country_keyboard())
            await state.set_state(AdminStates.waiting_for_country_to)
        else:
            await message.answer('Неправильный формат, используйте только русские или латинские буквы.')
    else:
        await state.set_state(AdminStates.waiting_for_country_from)
        await message.answer('Выберите из какой страны вы летите.',reply_markup=get_country_keyboard())

@router.message(AdminStates.waiting_for_country_to)
async def country_to(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Город куда',
                             reply_markup=city_keyboard(country))
        await state.set_state(AdminStates.waiting_for_city_to)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(AdminStates.waiting_for_city_to)
async def city_to(message: Message, state: FSMContext):
    city = message.text.strip()
    data = await state.get_data()
    if city != "Назад":
        if city != data['city_from']:
            if isvalid_city(city):
                await state.update_data(city_to=city)
                await message.answer('Отправителю будет важно знать когда вы планируете перелет.',
                                     reply_markup=ReplyKeyboardRemove())
                await message.answer('Выберите дату: ', reply_markup=await SimpleCalendar().start_calendar())
                await state.set_state(AdminStates.waiting_for_date)
            else:
                await message.answer('Неправильный формат, используйте только русские или латинские буквы.')
        else:
            await message.answer('Города отправления и назначения должны отличаться.')
    else:
        await state.set_state(AdminStates.waiting_for_country_to)
        await message.answer('Выберите в какую страну вы летите.', reply_markup=get_country_keyboard())


@router.callback_query(AdminStates.waiting_for_date, simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.delete()
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d/%m/%Y")}',
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(flight_date=str(date))
        await state.set_state(AdminStates.waiting_for_phone)
        await callback_query.message.answer('Номер телефона в формате +79997654321.')

@router.message(AdminStates.waiting_for_phone)
async def phone(message: Message, state: FSMContext):
    try:
        phone =  phonenumbers.parse(message.text.strip(), None)
        if phonenumbers.is_valid_number(phone) == True:
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            await state.update_data(phone=phone)
            await message.answer('Примечание')
            await state.set_state(AdminStates.waiting_for_info)
        else:
            await message.answer('Номер телефона введен в неправильном формате, попробуйте еще раз.')
    except phonenumbers.NumberParseException:
        await message.answer('Номер телефона введен в неправильном формате, попробуйте еще раз.')

@router.message(AdminStates.waiting_for_info)
async def info(message: Message, state: FSMContext):
    info = message.text.strip()
    if isvalid_info(info):
        await state.update_data(info=message.text.strip())
        data = await state.get_data()
        await message.answer(f"Вы ввели следующие данные:\nИмя: {data['user_name']}\nОткуда: {data['city_from']}\n"
                             f"Куда: {data['city_to']}\nДата: {(isoparse(data['flight_date'])).strftime('%d.%m.%Y')}\n"
                             f"Телефон: {data['phone']}\n"
                             f"Примечание: {data['info']}", reply_markup=get_valid_kb())
        await state.set_state(AdminStates.validate)
    elif len(info) > 200:
        await message.answer('Сообщение слишком длинное, сократите его.')
    else:
        await message.answer('Неправильный формат, используйте только русские или латинские буквы.')

@router.message(AdminStates.validate, Text(text="Все правильно", ignore_case=True))
async def write_db(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    data = await state.get_data()
    await session.execute(insert(
        Courier).values(
            user_id=data['user_id'],
            user_name = data['user_name'],
            city_from=data['city_from'],
            city_to=data['city_to'],
            flight_date=isoparse(data['flight_date']),
            phone=data['phone'],
            info=data['info'],
            status=True
        )
    )
    await session.commit()
    await message.answer('Данные записаны', reply_markup=get_to_start_kb())

    text = f'<b><a href="tg://user?id={data["user_id"]}">{data["user_name"]}</a></b> '\
           f"летит {isoparse(data['flight_date']).strftime('%d.%m.%Y')} по маршруту:\n"\
           f"{data['city_from']} ✈ {data['city_to']}\n"\
           f"<b>Примечание:</b> {data['info']}"
    await bot.send_message(chat_id=settings.AIR_CHAT_ID, text=text, reply_markup=to_bot(data["user_id"]))
    await state.clear()