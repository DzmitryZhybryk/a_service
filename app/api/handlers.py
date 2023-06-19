"""Module for storage AuthenticationHandler class"""

from app.api import schemas
from app.api.services import AuthenticationStorage


class AuthenticationHandlers:
    """
    Class contains handlers for requests to the API authentication service

    Methods:
        registrate_user: method registrations new user
        confirm_registration: method confirm registrations new user

    Args:
        storage: an instance of a class that works with storages

    """

    def __init__(self, storage: AuthenticationStorage) -> None:
        self.__services = storage

    async def registrate_user(self, user_data: schemas.RegistrateUser) -> schemas.RegistrateResponse:
        """
        Method registers new user.

        Args:
            user_data: pydantic model with new user data

        Returns
            pydantic model with data for confirm registration

        """
        new_user = await self.__services.add_user_to_database(user_data=user_data)
        return new_user

    async def confirm_registration(self, activate_key: str) -> schemas.ResponseToken:
        """
        Method confirms user registration

        Args:
            activate_key: key for activate new user

        Returns:
            pydantic model with credentials for authenticate

        """
        tokens = await self.__services.activate_person_in_database(activate_key=activate_key)
        return tokens
