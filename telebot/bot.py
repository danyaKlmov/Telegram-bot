import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import common, choosing_portals
from parsers.rss import rss_channels
from parsers.parse import parse_all


async def main():
    """
    Точка входа в бота.
    Запускается в asyncio.run()
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )

    dp = Dispatcher(storage=MemoryStorage())

    # Забираем токен из .env-файла
    bot = Bot(config.bot_token.get_secret_value())

    # Роутеры - новая фишка в бете 3.0+
    # Позволяет группировать хэндлеры
    # и выстраивать цепочку из них
    # https://docs.aiogram.dev/en/dev-3.x/dispatcher/router.html
    dp.include_router(common.router)
    dp.include_router(choosing_portals.router)

    # Парсим свежие новости при запуске бота.
    await parse_all(rss_channels.values())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
