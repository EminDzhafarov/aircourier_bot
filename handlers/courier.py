from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.courier import CourierStates
from filters.blacklist import BlacklistFilter
from utils.misc.validators import isvalid_name
from keyboards.citypicker import get_country_keyboard, city_keyboard, cities_by_country
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
    if isvalid_name(name) == True:
        await state.update_data(user_name=name)
        await message.answer(f'Очень приятно, {name}! Выберите из какой страны вы летите.', reply_markup=get_country_keyboard())
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


