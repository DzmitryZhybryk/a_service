"""Модуль для хранения Password класса, для работы с паролями"""
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi import HTTPException, status

from app.api import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:
    """
    Класс для работы с паролями
    """

    def __init__(self, password: str):
        self.__password = password

    def hash_password(self) -> str:
        """
        Метод для хеширования пароля

        Returns:
            Хешированный пароль

        """
        return pwd_context.hash(self.__password)

    def verify_password(self, hashed_password: str) -> bool:
        """
        Метод для проверки пароля

        Args:
            hashed_password: Хешированный пароль

        Returns:
            True - если пароль верный, False - если пароль не верный

        """
        try:
            is_verify = pwd_context.verify(self.__password, hashed_password)
            if not is_verify:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=schemas.IncorrectLoginData)

            return is_verify
        except UnknownHashError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=schemas.IncorrectLoginData)
