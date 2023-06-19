"""Storage module of the RedisWorker class that implements work with the Redis database"""
from typing import AsyncGenerator

import redis.asyncio as redis

from app.config import config
from app.utils import decorators


class RedisWorker:
    """
    The class implements work with Redis database

    Methods:
        connect
        hmset_data
        hgetall_data
        set_data
        get_data

    Args:
        host: redis database host
        password: redis user password
        db: redis database number
        username: redis database user

    """

    def __init__(self, host: str, password: str, db: int, username: str = None) -> None:
        self.__host = host
        self.__db = db
        self.__password = password
        self.__username = username

    async def connect(self) -> AsyncGenerator:
        """Method returns Redis database connect"""
        redis_db = redis.Redis.from_url(url=self.__host, db=self.__db, password=self.__password)
        try:
            yield redis_db
        finally:
            await redis_db.close()

    @decorators.redis_exceptions_handler
    async def hmset_data(self, name: str, mapping: dict) -> None:
        """
        Method insert dict to Redis database

        Args:
            name: key to select the data set in the future
            mapping: inserting data

        Raises:
            HTTP_500_INTERNAL_SERVER_ERROR if database connect not available

        """
        async for connect in self.connect():
            await connect.hmset(name=name, mapping=mapping)

    @decorators.redis_exceptions_handler
    async def hgetall_data(self, name: str) -> dict:
        """
        Method select dict from Redis database

        Args:
            name: key to select the data set

        Raises:
            HTTP_500_INTERNAL_SERVER_ERROR if database connect not available

        Returns:
            dict with data from Redis

        """
        async for connect in self.connect():
            response = await connect.hmgetall(name=name)
            return response

    @decorators.redis_exceptions_handler
    async def set_data(self, name: str, value: str) -> None:
        """
        Method insert string to Redis database

        Args:
            name: key to select the data set in the future
            value: inserting data

        Raises:
            HTTP_500_INTERNAL_SERVER_ERROR if database connect not available

        """
        async for connect in self.connect():
            await connect.set(name=name, value=value)

    @decorators.redis_exceptions_handler
    async def get_data(self, name: str) -> str:
        """
        Method select value from Redis database

        Args:
            name: key to select the value

        Raises:
            HTTP_500_INTERNAL_SERVER_ERROR if database connect not available

        Returns:
            value with data from Redis

        """
        async for connect in self.connect():
            response = await connect.get(name=name)
            return response


redis_storage = RedisWorker(host=config.database.redis_host, password=config.database.redis_password,
                            db=config.database.redis_database)
