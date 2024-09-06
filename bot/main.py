import asyncio
from bot_init import dp, bot  # Импортируем диспетчер и бота из bot_init.py
from bot.handlers import router  # Импортируем router из handlers.py
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Bot is starting...")

# Подключаем router к диспетчеру
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



