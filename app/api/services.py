from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Role, User


class AuthenticationStorage:

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__role_model = Role
        self.__user_mode = User

    async def create_init_roles(self):
        stmt = insert(Role).values(role="test45")
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def create_init_user(self):
        pass

    async def test1(self):
        stmt = insert(Role).values(role="test2")
        await self.__session.execute(stmt)
        await self.__session.commit()
