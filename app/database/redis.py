import redis.asyncio as redis
from app.config import database_config


class RedisWorker:

    def __init__(self, host: str, password: str, db: int, username: str = None):
        self.__host = host
        self.__db = db
        self.__password = password
        self.__username = username
        # self.__database_url = f"{host}{db}"

    def connect(self):
        redis_db = redis.Redis.from_url(url=self.__host, db=self.__db, password=self.__password)
        try:
            yield redis_db
        finally:
            redis_db.close()


test = RedisWorker(host=database_config.redis_host, password=database_config.redis_password,
                   db=database_config.redis_token_db)

redis_db = redis.Redis.from_url(url=database_config.redis_host, db=database_config.redis_token_db,
                                password=database_config.redis_password)
