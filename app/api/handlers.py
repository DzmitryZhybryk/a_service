"""Module for storage AuthenticationHandler class"""
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
