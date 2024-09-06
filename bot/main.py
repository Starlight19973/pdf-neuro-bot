import asyncio
from bot_init import dp, bot
from bot.handlers import router
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Bot is starting...")


dp.include_router(router)


async def main():
    try:
        # Запуск поллинга бота
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию бота после завершения
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())



