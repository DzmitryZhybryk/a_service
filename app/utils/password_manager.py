"""Модуль для хранения Password класса, для работы с паролями"""
from fastapi import HTTPException, status
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.api import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:
    """
    Class works with passwords

    Args:
        password: password for work

    """

    def __init__(self, password: str):
        self.__password = password

    def hash_password(self) -> str:
        """
        Method hashes passwords

        Returns:
            hashed password

        """
        return pwd_context.hash(self.__password)

    def verify_password(self, hashed_password: str) -> bool:
        """
        Method verifications passwords

        Args:
            hashed_password: hashed password

        Returns:
            True - if the password is correct, False - if not

        """
        try:
            is_verify = pwd_context.verify(self.__password, hashed_password)
            if not is_verify:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=schemas.IncorrectLoginData)

            return is_verify
        except UnknownHashError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=schemas.IncorrectLoginData)
