import redis.asyncio as redis

from app.config import database_config
from app.utils import decorators


class RedisWorker:

    def __init__(self, host: str, password: str, db: int, username: str = None):
        self.__host = host
        self.__db = db
        self.__password = password
        self.__username = username

    async def connect(self):
        redis_db = redis.Redis.from_url(url=self.__host, db=self.__db, password=self.__password)
        try:
            yield redis_db
        finally:
            await redis_db.close()

    @decorators.redis_exceptions_handler
    async def hmset_data(self, name: str, mapping: dict) -> None:
        async for connect in self.connect():
            await connect.hmset(name=name, mapping=mapping)

    @decorators.redis_exceptions_handler
    async def hgetall_data(self, name: str) -> dict:
        async for connect in self.connect():
            response = await connect.hmgetall(name=name)
            return response


refresh_token_storage = RedisWorker(host=database_config.redis_host, password=database_config.redis_password,
                                    db=database_config.redis_token_db)
