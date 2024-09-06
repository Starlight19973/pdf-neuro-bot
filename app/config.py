from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import redis.asyncio as redis
import os

# Загрузка переменных окружения из файла .env
load_dotenv()


class Settings(BaseSettings):
    bot_token: str
    db_url: str
    redis_url: str
    gemini_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
redis_instance = redis.from_url(settings.redis_url)
