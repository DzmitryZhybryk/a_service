import redis.asyncio as redis

from app.config import config
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

    @decorators.redis_exceptions_handler
    async def set_data(self, name: str, value: str) -> None:
        async for connect in self.connect():
            await connect.set(name=name, value=value)

    @decorators.redis_exceptions_handler
    async def get_data(self, name: str) -> str:
        async for connect in self.connect():
            response = await connect.get(name=name)
            return response


redis_storage = RedisWorker(host=config.database.redis_host, password=config.database.redis_password,
                            db=config.database.redis_database)
