from aiogram import Router
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.start import get_start_kb
from bot.keyboards.inline import send_msg
from bot.filters.blacklist import BlacklistFilter
from bot.filters.flights import FlightsFilter
from bot.states.start_states import StartStates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.db.models import Stats, Courier
from datetime import datetime

router = Router()

@router.message(Command("start"), BlacklistFilter(), FlightsFilter())
async def cmd_start(
    message: Message,
    flights: bool,
    state: FSMContext,
    session: AsyncSession,
    command: CommandObject
) -> None:
    """
    Хэндлер на команду /start, также принимает Deep Link
    :param message:
    :param flights:
    :param state:
    :param session:
    :param command:
    :return:
    """
    stats_query = await session.execute(select(Stats).where(Stats.user_id == message.from_user.id))
    if not stats_query.scalar():
        await session.merge(Stats(user_id=message.from_user.id, timestamp=datetime.now()))
        await message.answer("Привет! Этот бот поможет найти попутчиков для доставки посылок самолетом.\n\n" \
                             "<i>Отправляя сообщение, вы соглашаетесь на обработку персональных данных.</i>\n\n"
                             "Кстати, теперь у нас есть своя группа, где публикуются перелеты курьеров, "
                             "подписывайтесь, чтобы ничего не пропустить: @aircourier_chat")

    today = datetime.today()
    if command.args: # Получение аргумента из deep link, если таковой есть
        try:
            query = (await session.scalars(select(Courier)
                                           .where(Courier.user_id == int(command.args))
                                           .where(Courier.flight_date >= today)
                                           .where(Courier.status == True)
                                           .order_by(Courier.flight_date))).all()
            if query:
                for courier in query:
                    await message.answer(f'<b>{courier.city_from} ✈ {courier.city_to}</b>\n'
                                         f'<b>Дата:</b> {courier.flight_date.strftime("%d.%m.%Y")}'
                                         f'\n<b>Имя:</b> <a href="tg://user?id={courier.user_id}">'
                                         f'{courier.user_name}</a>\n'
                                         f'<b>Контакт:</b> {courier.phone}\n'
                                         f'<b>Примечание:</b> {courier.info}',
                                         reply_markup=send_msg(courier.phone))
                await message.answer(
                    "Обратите внимание: некоторые курьеры запрещают писать себе настройками "
                    "приватности, но вы можете добавить их в контакты по номеру телефона "
                    "или позвонить.")
        except ValueError:
                pass
    await session.commit()
    await message.answer("Выберите что вы хотите сделать.", reply_markup=get_start_kb(flights))
    await state.set_state(StartStates.start)

@router.message(Text(text="В начало", ignore_case=True), BlacklistFilter(), FlightsFilter())
async def begin(message: Message, flights: bool, state: FSMContext) -> None:
    """
    Хэндлер для возврата в главное меню при нажатии кнопки "В начало" на клавиатуре
    :param message:
    :param flights:
    :param state:
    :return:
    """
    await state.set_state(StartStates.start)
    await message.answer("Выберите что вы хотите сделать.", reply_markup=get_start_kb(flights))