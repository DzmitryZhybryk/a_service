"""Module for storage AuthenticationHandler class"""
from app.api import schemas
from app.api.services import AuthenticationStorage


class AuthenticationHandlers:
    """
    Class contains handlers for requests to the API authentication service

    Args:
        storage: an instance of the AuthenticationStorage class

    """

    def __init__(self, storage: AuthenticationStorage) -> None:
        """Inits AuthenticationHandlers class"""
        self.__services = storage

    async def registrate_user(self, user_data: schemas.RegistrateUser) -> None:
        """
        Method registrate new user

        Args:
            user_data: pydantic model with new user data

        """
        await self.__services.add_user_to_db(user_data=user_data)

    async def confirm_registration(self, email: str) -> None:
        """
        Method confirms user registration

        Args:
            email: user email address

        Returns:

        """
        await self.__services.activate_person_in_database(email=email)
