"""Module for storage dependencies"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.handlers import AuthenticationHandlers
from app.api.services import AuthenticationStorage
from app.database.db import use_session


def authentication_storage(session: AsyncSession = Depends(use_session)) -> AuthenticationStorage:
    """
    Dependency, used as a handle for work with AuthenticationStorage

    Args:
        session: database session

    Returns:
        an instance of the AuthenticationStorage class

    """
    return AuthenticationStorage(session=session)


def authentication_handler(storage: AuthenticationStorage = Depends(authentication_storage)) -> AuthenticationHandlers:
    """
    Dependency, used as a handle for work with AuthenticationHandlers

    Args:
        storage: an instance of the AuthenticationStorage class

    Returns:
        an instance of the AuthenticationHandlers class

    """
    return AuthenticationHandlers(storage=storage)
