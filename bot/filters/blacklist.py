from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud import get_blacklist


class BlacklistFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        user_id = message.from_user.id
        status = await get_blacklist(session, user_id)
        return not status == user_id