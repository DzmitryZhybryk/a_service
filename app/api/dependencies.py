"""Module for storage dependencies"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.handlers import AuthenticationHandlers
from app.api.services import AuthenticationStorage, PostgresStorage
from app.database.postgres import use_session
from app.database.redis import redis_storage


def postgres_storage(session: AsyncSession = Depends(use_session),
                     cache_database=redis_storage) -> PostgresStorage:
    """
    Dependency, takes database session and used as a handle for work in AuthenticationStorage class.

    Args:
        session: main database session (postgres)
        cache_database: database connection to work with fast cache memory (redis)

    Returns:
        an instance of the AuthenticationStorage class

    """
    return PostgresStorage(session=session, cache_database=cache_database)


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
