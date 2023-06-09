"""Module for storage AuthenticationHandler class"""
from app.api.services import AuthenticationStorage

from app.api import schemas
from app.database.models import User


class AuthenticationHandlers:
    """
    Class contains handlers for requests to the API authentication service

    Args:
        storage: an instance of the AuthenticationStorage class

    """

    def __init__(self, storage: AuthenticationStorage) -> None:
        """Inits AuthenticationHandlers class"""
        self.__services = storage

    async def registrate_user(self, user_data: schemas.RegistrateUser):
        """
        Method registrate new user

        Args:
            user_data: pydantic model with new user data

        Returns:
            pydantic model with registered user data

        """
        await self.__services.add_user_to_db(user_data=user_data)

