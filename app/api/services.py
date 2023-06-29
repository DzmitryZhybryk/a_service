"""Module for storage AuthenticationStorage class"""
from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api import schemas
from app.database.models import Role, User
from app.database.redis import RedisWorker
from app.utils import decorators
from app.utils.funcs import make_confirm_registration_key
from app.utils.oauth2 import JWTManager
from app.utils.password_manager import PasswordManager


class BaseStorage(ABC):
    """
    Abstract class, implements the storage interface

    Methods:
        add_user_to_database: method insert new user to database
        activate_person_in_database: method activate new user in the database
        get_user_by_id: method selects user from database by user id

    """

    @abstractmethod
    async def add_user_to_database(self, user_data: schemas.RegistrateUser) -> schemas.RegistrateResponse:
        """
        Method gets new user data and insert it to database

        Args:
            user_data: pydantic model with new user data

        """
        pass

    @abstractmethod
    async def activate_person_in_database(self, activate_key: str) -> schemas.ResponseToken:
        """
        Method gets the user's email and activate that user in the database

        Args:
            activate_key: key for activate new user

        Returns:
            pydantic model with tokens and tokens type

        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> schemas.GetUserResponse:
        """
        Method selects user in database by user id

        Args:
            user_id: user identification key in a database

        Returns:
            pydantic model with user data

        """
        pass


class PostgresStorage(BaseStorage):
    """
    Class extends BaseStorage class and contains methods for work with external storages

    Methods:
        add_user_to_database: method insert new user to database
        activate_person_in_database: method activate new user in the database
        get_user_by_id: method selects user from database by user id

    Args:
        session: main database session (postgres)
        cache_database: database connection to work with fast cache memory (redis)

    """

    def __init__(self, session: AsyncSession, cache_database: RedisWorker) -> None:
        """Inits AuthenticationStorage class"""
        self.__session = session
        self.__cache_database = cache_database
        self.__role_model = Role
        self.__user_model = User
        self.__jwt_worker = JWTManager()

    async def __select_role(self, role: str, raise_not_found=False) -> Role | None:
        """
        Method gets user's role and find this role in the database

        Args:
            role: role to select from database
            raise_not_found: if False - return None if user is not found in the database, return exception if True

        Raises:
            HTTP_500_INTERNAL_SERVER_ERROR if user already exist in database

        Returns:
            role from database

        """
        stmt = select(self.__role_model).where(Role.role == role)
        result = await self.__session.scalar(stmt)
        if not result and raise_not_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role} not found")

        return result

    @decorators.integrity_error_handler
    async def add_user_to_database(self, user_data: schemas.RegistrateUser) -> schemas.RegistrateResponse:
        """Overrides base class method"""
        user_role = await self.__select_role(role=user_data.role, raise_not_found=True)
        hashed_password = PasswordManager(password=user_data.password).hash_password()
        stmt = insert(User).returning(User).values(role_id=user_role.id, password=hashed_password,
                                                   **user_data.dict(exclude={"role", "password", "confirm_password"}))
        response = await self.__session.execute(stmt)
        registered_user = response.scalar_one()
        await self.__session.commit()
        confirm_registration_key = make_confirm_registration_key(_range=20)
        await self.__cache_database.set_data(name=confirm_registration_key, value=registered_user.id)

        response_schema = schemas.RegistrateResponse(username=registered_user.username, email=registered_user.email,
                                                     confirm_registration_key=confirm_registration_key)
        return response_schema

    def __make_tokens(self, user: User) -> tuple[str, str]:
        """
        Method gets user data and make tuple with access and refresh tokens

        Args:
            user: pydantic model with user data from database

        Returns:
            access token, refresh token

        """
        access_token = self.__jwt_worker.create_access_token(role=user.role.role, username=user.username,
                                                             user_id=user.id)
        refresh_token = self.__jwt_worker.create_refresh_token()
        return access_token, refresh_token

    async def activate_person_in_database(self, activate_key: str) -> schemas.ResponseToken:
        """Overrides base class method"""
        user_id = await self.__cache_database.get_data(name=activate_key)
        stmt = update(self.__user_model).returning(User).where(User.id == int(user_id)).values(
            is_user_activate=True).options(selectinload(User.role))
        response = await self.__session.execute(stmt)
        activated_user = response.scalar_one()
        await self.__session.commit()
        access_token, refresh_token = self.__make_tokens(user=activated_user)
        await self.__cache_database.hmset_data(name=refresh_token,
                                               mapping={"username": activated_user.username, "id": activated_user.id,
                                                        "role": activated_user.role.role})

        response_schema = schemas.ResponseToken(access_token=access_token, refresh_token=refresh_token)
        return response_schema

    async def get_user_by_id(self, user_id: int, raise_not_found: bool = True) -> schemas.GetUserResponse:
        """Overrides base class method"""
        stmt = select(self.__user_model).where(User.id == user_id).options(selectinload(User.role))
        result = await self.__session.scalar(stmt)
        if not result and raise_not_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with user_id: {user_id} not found")

        print("###############")
        print(type(result.birthday))
        response_schema = schemas.GetUserResponse(**result.dict())
        return response_schema


class AuthenticationStorage:
    """
    The class implements the logic of working with storage

    Methods:
        add_user_to_database: method insert new user to database
        activate_person_in_database: method activate new user in the database
        get_user_by_id: method selects user from database by user id

    Args:
        database_storage: class which implements logic of working with database storage

    """

    def __init__(self, database_storage: BaseStorage) -> None:
        self.__storage = database_storage

    async def add_user_to_database(self, user_data: schemas.RegistrateUser) -> schemas.RegistrateResponse:
        """Method implements BaseStorage logic"""
        return await self.__storage.add_user_to_database(user_data=user_data)

    async def activate_person_in_database(self, activate_key: str) -> schemas.ResponseToken:
        """Method implements BaseStorage logic"""
        return await self.__storage.activate_person_in_database(activate_key=activate_key)

    async def get_user_by_id(self, user_id: int) -> schemas.GetUserResponse:
        """Method implements BaseStorage logic"""
        return await self.__storage.get_user_by_id(user_id=user_id)
