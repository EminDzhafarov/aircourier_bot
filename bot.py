import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.start import get_start_kb
from handlers import courier, sender, admin
from filters.blacklist import BlacklistFilter
from settings import TG_TOKEN

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TG_TOKEN, parse_mode="HTML")
# Память
storage = MemoryStorage()
# Диспетчер
dp = Dispatcher()
dp.include_routers(courier.router, sender.router)
# База данных
# loop = asyncio.get_event_loop()
# db = Database(loop)

# Хэндлер на команду /start
@dp.message(BlacklistFilter(), Command("start"))
async def cmd_start(message: types.Message) -> None:
        await message.answer("Привет! Этот бот поможет найти попутчиков для доставки посылок самолетом.\n\n"\
                "<i>Отправляя сообщение, вы соглашаетесь на обработку персональных данных.</i>\n\n"\
                "Для начала выберите"\
                             " что вы хотите сделать.", reply_markup=get_start_kb())

# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())