"""Storage module for Dependencies"""
from app.api.handlers import AuthenticationHandlers
from app.api.services import AuthenticationStorage
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.db import use_session


def authentication_storage(session: AsyncSession = Depends(use_session)) -> AuthenticationStorage:
    return AuthenticationStorage(session=session)


def authentication_handler(storage: AuthenticationStorage = Depends(authentication_storage)) -> AuthenticationHandlers:
    """
    Dependency, используется как ручка для работы с роутами Employee

    Args:
        storage: Экземпляр класса PersonStorage c моделями баз данных  Person, Photo

    Returns:
        экземпляр класса PersonHandlers

    """
    return AuthenticationHandlers(storage=storage)
