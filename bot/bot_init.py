from aiogram import Bot, Dispatcher
from app.config import settings
from aiogram.fsm.storage.redis import RedisStorage

# Инициализация бота
bot = Bot(token=settings.bot_token)

# Инициализация хранилища состояний через Redis
storage = RedisStorage.from_url(settings.redis_url)

# Инициализация диспетчера с использованием Redis хранилища
dp = Dispatcher(storage=storage)
