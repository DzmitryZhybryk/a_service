"""Module for storage AuthenticationStorage class"""
from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api import schemas
from app.config import config
from app.database.models import Role, User
from app.database.redis import RedisWorker
from app.utils import decorators
from app.utils.funcs import make_confirm_registration_key
from app.utils.oauth2 import JWTManager
from app.utils.password_manager import PasswordManager


class AuthenticationStorage:
    """
    Class contains methods for work with external storage

    Args:
        session: database session
        cache_database: cache database connect

    """

    def __init__(self, session: AsyncSession, cache_database: RedisWorker) -> None:
        """Inits AuthenticationStorage class"""
        self.__session = session
        self.__cache_database = cache_database
        self.__role_model = Role
        self.__user_mode = User
        self.__jwt_worker = JWTManager()

    async def __is_role_exist(self) -> bool:
        """
        Method checks if the roles exist in the database

        Returns: true if there are roles in database table, false if not

        """
        stmt = select(self.__role_model)
        role = await self.__session.scalar(stmt)
        return bool(role)

    async def __is_user_exist(self) -> bool:
        """
        Method checks if the users exist in the database

        Returns: true if there are users in database table, false if not

        """
        stmt = select(self.__user_mode)
        user = await self.__session.scalar(stmt)
        return bool(user)

    async def __create_init_roles(self) -> None:
        """
        Method adds init roles to the database

        """
        if not await self.__is_role_exist():
            user_roles = config.init.user_roles
            for role in user_roles:
                stmt = insert(Role).values(role=role)
                await self.__session.execute(statement=stmt)
                await self.__session.commit()

    async def __get_role(self, role: str, raise_not_found=False) -> Role | None:
        """
        Method gets user's role and find this role in the database

        Args:
            role: role to select from database
            raise_not_found: if False - return None if user is not found in the database, return exception if True

        Returns:
            role from database

        """
        stmt = select(self.__role_model).where(Role.role == role)
        result = await self.__session.scalar(stmt)
        if not result and raise_not_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role} not found")

        return result

    async def __creat_init_user(self) -> None:
        """
        Method adds init user to database

        """
        if not await self.__is_user_exist():
            init_user_role = await self.__get_role(role=config.init.role, raise_not_found=True)
            hashed_password = PasswordManager(password=config.init.password).hash_password()
            stmt = insert(User).values(username=config.init.username, password=hashed_password,
                                       nickname=config.init.nickname, email=config.init.email,
                                       role_id=init_user_role.id, is_user_activate=True)
            await self.__session.execute(statement=stmt)
            await self.__session.commit()

    async def create_init_database_data(self) -> None:
        """
        Method adds init database data

        """
        await self.__create_init_roles()
        await self.__creat_init_user()

    @decorators.integrity_error_handler
    async def add_user_to_db(self, user_data: schemas.RegistrateUser) -> schemas.RegistrateResponse:
        """
        Method gets new user data and adds it to database

        Args:
            user_data: pydantic model with new user data

        """
        user_role = await self.__get_role(role=user_data.role, raise_not_found=True)
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
        access_token = self.__jwt_worker.create_access_token(role=user.role.role, username=user.username,
                                                             user_id=user.id)
        refresh_token = self.__jwt_worker.create_refresh_token()
        return access_token, refresh_token

    async def activate_person_in_database(self, activate_key: str) -> schemas.ResponseToken:
        """
        Method gets the user's email and activate that user in the database

        Args:
            activate_key: key for activate new user

        Returns:
            pydantic model with tokens and tokens type

        """
        user_id = await self.__cache_database.get_data(name=activate_key)
        stmt = update(self.__user_mode).returning(User).where(User.id == int(user_id)).values(
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
