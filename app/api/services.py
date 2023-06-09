"""Module for storage AuthenticationStorage class"""
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schemas
from app.config import base_config, init_config
from app.database.models import Role, User
from app.utils import decorators
from app.utils.funcs import make_confirm_registration_url
from app.utils.mail import mail_worker
from app.utils.password_manager import PasswordManager
from app.utils.serializer import serializer


class AuthenticationStorage:
    """
    Class contains methods for work with external storage

    Args:
        session: database session

    """

    def __init__(self, session: AsyncSession) -> None:
        """Inits AuthenticationStorage class"""
        self.__session = session
        self.__role_model = Role
        self.__user_mode = User

    async def __is_role_exist(self) -> bool:
        """
        Method checks if the role exist in the database

        Returns: true if there are roles in database table, false if not

        """
        stmt = select(self.__role_model)
        role = await self.__session.scalar(stmt)
        return bool(role)

    async def __is_user_exist(self) -> bool:
        """
        Method checks if the user exist in the database

        Returns: true if there are users in database table, false if not

        """
        stmt = select(self.__user_mode)
        user = await self.__session.scalar(stmt)
        return bool(user)

    async def __create_init_roles(self) -> None:
        """
        Method create init roles in database

        """
        if not await self.__is_role_exist():
            user_roles = base_config.user_roles
            for role in user_roles:
                stmt = insert(Role).values(role=role)
                await self.__session.execute(statement=stmt)
                await self.__session.commit()

    async def __get_role(self, role: str) -> Role:
        """
        Method get user role from database

        Args:
            role: role for select from database

        Returns:
            Role object

        """
        stmt = select(self.__role_model).where(Role.role == role)
        result = await self.__session.scalar(stmt)
        return result

    async def __creat_init_user(self) -> None:
        """
        Method create init user in database

        """
        if not await self.__is_user_exist():
            init_user_role = await self.__get_role(role=init_config.role)
            hashed_password = PasswordManager(password=init_config.password).hash_password()
            stmt = insert(User).values(username=init_config.username, password=hashed_password,
                                       nickname=init_config.nickname, email=init_config.email,
                                       role_id=init_user_role.id, is_user_activate=True)

            await self.__session.execute(statement=stmt)
            await self.__session.commit()

    async def create_init_database_data(self) -> None:
        """
        Method create init database data

        """
        await self.__create_init_roles()
        await self.__creat_init_user()

    @decorators.integrity_error_handler
    async def add_user_to_db(self, user_data: schemas.RegistrateUser) -> None:
        """
        Method add user to database

        Args:
            user_data: pydantic model with new user data

        Returns:
            pydantic model with add user data

        """
        user_role = await self.__get_role(role=user_data.role)
        hashed_password = PasswordManager(password=user_data.password).hash_password()
        stmt = insert(User).returning(User).values(role_id=user_role.id, password=hashed_password,
                                                   **user_data.dict(exclude={"role", "password", "confirm_password"}))
        await self.__session.execute(stmt)
        serialize_email = serializer.serialize_secret_data(secret_data=user_data.email)
        confirm_registration_url = make_confirm_registration_url(user_mail=serialize_email)
        mail_worker.send_mail(recipient=user_data.email, send_data=confirm_registration_url,
                              subject="Confirm registration")
        await self.__session.commit()

    async def activate_person_in_database(self, mail: str):
        user_email = serializer.deserialize_secret_data(secret_data=mail)
        from sqlalchemy.orm import selectinload
        # stmt = select(self.__user_mode).where(User.email == user_email).options(selectinload(User.role))
        stmt = update(self.__user_mode).where(User.email == user_email).values(is_user_activate=True)
        await self.__session.execute(stmt)
        await self.__session.commit()
        # print("###############")
        # print(user)