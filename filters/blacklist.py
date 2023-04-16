from aiogram.filters import BaseFilter
from aiogram.types import Message


class BlacklistFilter(BaseFilter):
    def __init__(self, user_id):
        self.user_id = user_id

    async def __call__(self, message: Message) -> bool:
        status = '''SQL запрос'''
        return status == self.user_id