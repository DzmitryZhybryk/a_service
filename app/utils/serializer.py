"""Module for storage Serialize class"""
from fastapi import HTTPException, status
from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadSignature

from app.config import config


class Serializer:
    """Class for work with secret data"""

    def __init__(self):
        self.__secret_key = config.secret.secret_key
        self.__salt = config.secret.salt
        self.__worker = URLSafeSerializer(secret_key=self.__secret_key, salt=self.__salt)

    def serialize_secret_data(self, **kwargs) -> dict:
        """
        Method get secret data and serialize it

        Args:
            kwargs: secret data for serialize

        Returns:
            serialized data

        """
        for key, value in kwargs.items():
            kwargs[key] = self.__worker.dumps(value)
        return kwargs

    def deserialize_secret_data(self, **kwargs) -> dict:
        """
        Method get serialized data and deserialize it

        Args:
            kwargs: secret data for deserialize

        Returns:
            deserialized data

        """
        try:
            for key, value in kwargs.items():
                kwargs[key] = self.__worker.loads(value)
        except BadSignature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't deserialize this data")

        return kwargs


serializer = Serializer()
