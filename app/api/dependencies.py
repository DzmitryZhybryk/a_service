"""Module for storage dependencies"""
from fastapi import Depends, HTTPException, status
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.handlers import AuthenticationHandlers
from app.api.services import AuthenticationStorage, PostgresStorage
from app.config import config
from app.database.postgres import use_session
from app.database.redis import redis_storage


def postgres_storage(session: AsyncSession = Depends(use_session)) -> PostgresStorage:
    """
    Dependency, takes database session and used as a handle for work in AuthenticationStorage class.

    Args:
        session: main database session (postgres)

    Returns:
        an instance of the AuthenticationStorage class

    """
    return PostgresStorage(session=session, cache_database=redis_storage)


def authentication_storage(database_storage=Depends(postgres_storage)) -> AuthenticationStorage:
    return AuthenticationStorage(database_storage=database_storage)


def authentication_handler(storage: AuthenticationStorage = Depends(authentication_storage)) -> AuthenticationHandlers:
    """
    Dependency, takes an instance of the AuthenticationStorage class and used as a handle for work with
    AuthenticationHandlers class.

    Args:
        storage: an instance of the AuthenticationStorage class with database connections

    Returns:
        an instance of the AuthenticationHandlers class

    """
    return AuthenticationHandlers(storage=storage)


api_key_header = APIKeyHeader(name="X-API_Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == config.secret.api_key:
        return api_key

    raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid API key")
