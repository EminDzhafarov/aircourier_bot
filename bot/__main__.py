import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from handlers import courier_handlers, sender_handlers, admin_handlers, start_handlers, flights_handlers
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aioredis import Redis
from config_reader import config

# Запуск процесса поллинга новых апдейтов
async def main():
    # Объект бота
    bot = Bot(token=config.TG_TOKEN.get_secret_value(), parse_mode="HTML")
    # База данных
    engine = create_async_engine(url=config.DB_URL.get_secret_value(), echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO, filename="../log.log", filemode="w")
    # Redis
    redis = Redis()
    # Память
    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_bot_id=True))\
        .from_url(config.REDIS_URL.get_secret_value())
    # Диспетчер
    dp = Dispatcher(storage=storage)
    dp.include_routers(start_handlers.router,
                       courier_handlers.router,
                       sender_handlers.router,
                       flights_handlers.router,
                       admin_handlers.router)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())