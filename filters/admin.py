from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Admins

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        query = await session.execute(select(Admins.user_id).filter_by(user_id=message.from_user.id))
        status = query.scalar()
        await session.commit()
        return status == message.from_user.id