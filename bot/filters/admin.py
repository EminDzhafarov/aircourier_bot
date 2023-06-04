from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot.db.crud import get_admin
from sqlalchemy.ext.asyncio import AsyncSession


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        user_id = message.from_user.id
        status = await get_admin(session, user_id)
        return status == user_id
