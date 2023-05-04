from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Courier

class FlightsFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        query = (await session.execute(select(Courier).where(Courier.user_id == message.from_user.id).where(Courier.status == True))).all()
        if query:
            return {"flights": True}
        else:
            return {"flights": False}