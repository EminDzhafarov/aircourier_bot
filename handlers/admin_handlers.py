from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from keyboards.admin import get_admin_start, get_admin_add, get_admin_del
from keyboards.start import get_to_start_kb
from keyboards.inline import del_blacklist, DelBlacklist
from states.admin_states import AdminStates
from filters.admin import AdminFilter
from db.models import Blacklist

router = Router()

@router.message(Command("admin"), AdminFilter())
async def blacklist_start(message: Message, state: FSMContext):
    await state.set_state(AdminStates.start)
    await message.answer("Что нужно сделать?", reply_markup=get_admin_start())

@router.message(Text("Добавить"))
async def blacklist_add(message: Message, state: FSMContext):
    await state.set_state(AdminStates.add)
    await message.answer("Введите user_id", reply_markup=ReplyKeyboardRemove)

@router.message(AdminStates.add)
async def blacklist_add(message: Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    await state.set_state(AdminStates.add_validator)
    await message.answer(f"Подтвердите добавление {user_id} в черный список.", reply_markup=get_admin_add())

@router.message(Text("Подтверждаю добавление"))
async def blacklist_add(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(insert(Blacklist).values(user_id=data['user_id']))
    await session.commit()
    await state.clear()
    await message.answer("Пользователь добавлен в черный список.", reply_markup=get_to_start_kb())

@router.message(Text("Удалить"))
async def blacklist_add(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(AdminStates.delete)
    query = (await session.scalars(select(Blacklist))).all()
    await message.answer("Вот черный список:", reply_markup=get_to_start_kb())
    for users in query:
        await message.answer(f'<a href="tg://user?id={users.user_id}">{users.user_id}</a>', reply_markup=del_blacklist(users.user_id))


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