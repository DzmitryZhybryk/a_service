"""Storage module for Dependencies"""
from app.handlers import AuthenticationHandlers
from app.services import AuthenticationStorage
from fastapi import Depends


def authentication_storage() -> AuthenticationStorage:
    return AuthenticationStorage()


def authentication_handler(storage: AuthenticationStorage = Depends(authentication_storage)) -> AuthenticationHandlers:
    """
    Dependency, используется как ручка для работы с роутами Employee

    Args:
        storage: Экземпляр класса PersonStorage c моделями баз данных  Person, Photo

    Returns:
        экземпляр класса PersonHandlers

    """
    return AuthenticationHandlers(storage=storage)
