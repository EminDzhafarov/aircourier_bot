from aiogram.filters import BaseFilter
from aiogram.types import Message
from settings import ADMINS

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS