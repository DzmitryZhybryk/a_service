"""Module for storage class for work with OAuth2"""
from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.config import config

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class JWTManager:
    """
    Class works with JWT tokens

    Methods:
        create_access_token
        create_refresh_token

    """

    def __init__(self):
        self.__secret_key = config.secret.secret_key
        self.__algorithm = config.secret.jwt_algorithm

    def create_access_token(self, username: str, role: str, user_id: int) -> str:
        """
        Method creates new access token

        Args:
            username: user username from the database
            role: user role from the database
            user_id: database user ID

        Returns:
            access token

        """
        access_token_expire = datetime.utcnow() + timedelta(minutes=config.secret.access_token_expire)
        to_encode = {"sub": username, "role": role, "exp": access_token_expire, "user_id": user_id}
        encode_access_jwt = jwt.encode(claims=to_encode, key=self.__secret_key, algorithm=self.__algorithm)
        return encode_access_jwt

    def create_refresh_token(self) -> str:
        """Method creates and return new refresh token"""
        refresh_token_expire = datetime.utcnow() + timedelta(days=config.secret.refresh_token_expire)
        to_encode = {"exp": refresh_token_expire}
        encode_refresh_jwt = jwt.encode(claims=to_encode, key=self.__secret_key, algorithm=self.__algorithm)
        return encode_refresh_jwt
