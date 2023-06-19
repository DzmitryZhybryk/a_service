"""Module for storage decorators"""
from fastapi import HTTPException, status
from kombu.exceptions import OperationalError
from redis.exceptions import RedisError
from sqlalchemy.exc import IntegrityError


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

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RedisError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis connection problems")

    return wrapper


def operation_error_handler(func):
    """
    Decorator, handles Celery error

    Args:
        func: decorated function

    Returns:
        decorated function

    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't send task")

    return wrapper
