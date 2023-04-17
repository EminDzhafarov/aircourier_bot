from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.courier import CourierStates
from filters.blacklist import BlacklistFilter
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

@router.message(BlacklistFilter(), CourierStates.waiting_for_name)
async def courier_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(user_name=name)
    await message.answer(f'Очень приятно, {name}! Выберите из какой страны вы летите.')
    await state.set_state(CourierStates.waiting_for_country_from)