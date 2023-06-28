"""Module for storage AuthenticationHandler class"""

from app.api import schemas
from app.api import tasks
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

    async def activate_user(self, activate_key: str) -> schemas.ResponseToken:
        """
        Method activate user

        Args:
            activate_key: key for activate new user

        Returns:
            pydantic model with credentials for authenticate

        """
        tokens = await self.__services.activate_person_in_database(activate_key=activate_key)
        return tokens

    @staticmethod
    def confirm_registration(email: str, username: str, confirm_key: str) -> None:
        """
        Method send tasks for confirm registration user

        Args:
            email: user email for confirm registration
            username: user username
            confirm_key: key for confirm registration

        Returns:
            pydantic model with credentials for authenticate

        """
        tasks.send_confirm_registration_email.delay(email=email, username=username, confirm_key=confirm_key)

    async def get_user(self, user_id: int) -> schemas.GetUserResponse:
        """
        Method get user id and return user data

        Args:
            user_id: user identification key in a database

        Returns:
            pydantic model with user data

        """
        user = await self.__services.get_user_by_id(user_id=user_id)
        return user
