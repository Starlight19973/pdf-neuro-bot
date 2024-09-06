from app.config import redis_instance


# Для Redis: добавляем пользователя в множество
async def add_user_to_redis(user_id: int):
    await redis_instance.sadd("bot_users", user_id)


# Для Redis: получаем количество уникальных пользователей
async def get_user_count_redis():
    return await redis_instance.scard("bot_users")


# Для базы данных: добавляем пользователя в таблицу
async def add_user_to_db(user_id: int, session):
    # Добавляем пользователя в базу данных, если его нет
    await session.execute(
        "INSERT INTO bot_users (user_id) VALUES (:user_id) ON CONFLICT (user_id) DO NOTHING",
        {"user_id": user_id}
    )
    await session.commit()


# Для базы данных: получаем количество уникальных пользователей
async def get_user_count_db(session):
    result = await session.execute("SELECT COUNT(*) FROM bot_users")
    return result.scalar()