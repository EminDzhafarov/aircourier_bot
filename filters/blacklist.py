from aiogram.filters import BaseFilter
from aiogram.types import Message


class BlacklistFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        status = '''SQL запрос с user_id'''
        return not status == message.from_user.id