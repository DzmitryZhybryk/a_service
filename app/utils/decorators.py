"""Module for storage decorators"""
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from redis.exceptions import RedisError


def integrity_error_handler(func):
    """
    Decorator, handles integrity error

    Args:
        func: decorated function

    Returns:
        decorated function

    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="The same data already exist in database")

    return wrapper


def redis_exceptions_handler(func):
    """
    Decorator, handles Redis error

    Args:
        func: decorated function

    Returns:
        decorated function

    """

    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except RedisError as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis connection problems")

    return wrapper
