import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import courier_handlers, sender_handlers, admin_handlers, start_handlers, flights_handlers
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import TG_TOKEN, DB_URL

async def main():
    # База данных
    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=TG_TOKEN, parse_mode="HTML")
    # Память
    storage = MemoryStorage()
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(start_handlers.router,
                       courier_handlers.router,
                       sender_handlers.router,
                       flights_handlers.router,
                       admin_handlers.router)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    # Запуск процесса поллинга новых апдейтов

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())