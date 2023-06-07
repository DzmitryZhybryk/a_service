from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def integrity_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data already exist in database")
            pass

    return wrapper
