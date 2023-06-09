"""Module for storage Serialize class"""
from fastapi import HTTPException, status
from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadSignature

from app.config import secret_config


class Serializer:
    """Class for work with secret data"""

    def __init__(self):
        self.__secret_key = secret_config.secret_key
        self.__salt = secret_config.salt
        self.__worker = URLSafeSerializer(secret_key=self.__secret_key, salt=self.__salt)

    def serialize_secret_data(self, secret_data: str) -> str | bytes:
        """
        Method get secret data and serialize it

        Args:
            secret_data: secret data for serialize

        Returns:
            serialized data

        """
        data = self.__worker.dumps(secret_data)
        return data

    def deserialize_secret_data(self, secret_data: str | bytes) -> str:
        """
        Method get serialized data and deserialize it

        Args:
            secret_data: secret data for deserialize

        Returns:
            deserialized data

        """
        try:
            data = self.__worker.loads(secret_data)
        except BadSignature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't deserialize this data")
        return data


serializer = Serializer()
