"""Module for storage class for work with OAuth2"""
from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.config import secret_config

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class JWTManager:
    """
    Class works with JWT tokens
    """

    def __init__(self):
        self._secret_key = secret_config.secret_key
        self._algorithm = secret_config.jwt_algorithm

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
        access_token_expire = datetime.utcnow() + timedelta(days=secret_config.access_token_expire)
        data = {"sub": username, "role": role, "exp": access_token_expire, "user_id": user_id}
        to_encode = data.copy()
        encode_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encode_jwt
