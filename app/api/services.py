"""Module for storage AuthenticationStorage class"""
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import base_config, init_config
from app.database.models import Role, User
from app.utils.password_manager import PasswordManager


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
            stmt = insert(User).returning(User).values(username=init_config.username, password=hashed_password,
                                                       nickname=init_config.nickname, email=init_config.email,
                                                       role_id=init_user_role.id)

            await self.__session.execute(statement=stmt)
            await self.__session.commit()

    async def create_init_database_data(self) -> None:
        """
        Method create init database data

        """
        await self.__create_init_roles()
        await self.__creat_init_user()
