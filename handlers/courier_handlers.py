from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.courier_states import CourierStates
from filters.blacklist import BlacklistFilter
from utils.misc.validators import isvalid_name, isvalid_city, isvalid_info
from keyboards.citypicker import get_country_keyboard, city_keyboard, cities_by_country
from keyboards.calendar.simple_calendar import SimpleCalendarCallback as simple_cal_callback, SimpleCalendar

import phonenumbers

router = Router()

@router.message(BlacklistFilter(), Text(text="✈️ Хочу доставить", ignore_case=True))
async def courier_start(message: Message, state: FSMContext):
    await message.answer(
        'Вы выбрали роль курьера, нам нужно получить некоторую информацию о вас, чтобы передать '\
                'отправителю. Напишите как вас зовут.\n\n<i>Если вы допустили ошибку при заполнении формы, продолжайте'\
                ', в конце вы сможете ее обнулить и начать заново.</i>',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(CourierStates.waiting_for_name)

@router.message(CourierStates.waiting_for_name)
async def courier_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if isvalid_name(name):
        await state.update_data(user_name=name)
        await message.answer(f'Очень приятно, {name}! Выберите из какой страны вы летите.',\
                             reply_markup=get_country_keyboard())
        await state.set_state(CourierStates.waiting_for_country_from)
    else:
        await message.answer('Неправильный формат, используйте только русские или латинские буквы.')

@router.message(CourierStates.waiting_for_country_from)
async def country_from(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите из какого города вы летите.', \
                             reply_markup=city_keyboard(country))
        await state.set_state(CourierStates.waiting_for_city_from)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(CourierStates.waiting_for_city_from)
async def city_from(message: Message, state: FSMContext):
    city = message.text.strip()
    if isvalid_city(city):
        await state.update_data(city_from=city)
        await message.answer('Выберите в какую страну вы летите.', reply_markup=get_country_keyboard())
        await state.set_state(CourierStates.waiting_for_country_to)
    else:
        await message.answer('Неправильный формат, используйте только русские или латинские буквы.')

@router.message(CourierStates.waiting_for_country_to)
async def country_to(message: Message, state: FSMContext):
    country = message.text.strip()
    if country in cities_by_country:
        await message.answer(f'Выбрана страна {country}, теперь выберите в какой город вы летите.', \
                             reply_markup=city_keyboard(country))
        await state.set_state(CourierStates.waiting_for_city_to)
    else:
        await message.answer('Сервис пока не работает в этой стране.')

@router.message(CourierStates.waiting_for_city_to)
async def city_to(message: Message, state: FSMContext):
    city = message.text.strip()
    data = await state.get_data()
    if city != data['city_from']:
        if isvalid_city(city):
            await state.update_data(city_to=city)
            await message.answer('Отправителю будет важно знать когда вы планируете перелет.', \
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer('Выберите дату: ', reply_markup=await SimpleCalendar().start_calendar())
            await state.set_state(CourierStates.waiting_for_date)
        else:
            await message.answer('Неправильный формат, используйте только русские или латинские буквы.')
    else:
        await message.answer('Города отправления и назначения должны отличаться.')


@router.callback_query(CourierStates.waiting_for_date, simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.delete()
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d/%m/%Y")}',
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(flight_date=date)
        await state.set_state(CourierStates.waiting_for_phone)
        await callback_query.message.answer('Для надежности отправителю лучше знать ваш номер телефона. Не забудьте ' \
                                            'указать код страны. Пример: +79997654321.')

@router.message(CourierStates.waiting_for_phone)
async def phone(message: Message, state: FSMContext):
    try:
        phone =  phonenumbers.parse(message.text.strip(), None)
        if phonenumbers.is_valid_number(phone) == True:
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            await state.update_data(phone=phone)
            await message.answer('Отправителю будет полезно знать о том, что вы готовы брать с собой, а что не '\
                    'готовы.\n\nУкажите, например, сколько у вас доступно мест багажа, какие габариты посылки можете '\
                    'принять и т.д. \n\nЕстественно, брать с собой запрещенные к провозу вещества и предметы мы '\
                    'не советуем, также рекомендуем ознакомиться с правилами провоза багажа вашей авиакомпании.')
            await state.set_state(CourierStates.waiting_for_info)
        else:
            await message.answer('Номер телефона введен в неправильном формате, попробуйте еще раз.')
    except phonenumbers.NumberParseException:
        await message.answer('Номер телефона введен в неправильном формате, попробуйте еще раз.')

@router.message(CourierStates.waiting_for_info)
async def info(message: Message, state: FSMContext):
    info = message.text.strip()
    if isvalid_info(info):
        await state.update_data(info=message.text.strip())
        data = await state.get_data()
        await message.answer(f"Вы ввели следующие данные:\nИмя: {data['user_name']}\nОткуда: {data['city_from']}\n" \
                             f"Куда: {data['city_to']}\nДата: {(data['flight_date']).strftime('%d.%m.%Y')}\nТелефон: {data['phone']}\n" \
                             f"Примечание: {data['info']}")
        await state.clear()
    elif len(info) > 200:
        await message.answer('Сообщение слишком длинное, сократите его.')
    else:
        await message.answer('Неправильный формат, используйте только русские или латинские буквы.')