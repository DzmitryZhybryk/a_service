"""Module for storage decorators"""
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def integrity_error_handler(func):
    """
    Decorator, handles integrity error

    Args:
        func: decorated function

    Returns:

    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The same data already exist in database")

    return wrapper
