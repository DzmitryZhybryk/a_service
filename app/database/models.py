"""Module for storage database models"""
import datetime

from fastapi import HTTPException, status
from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint, Date, Boolean
from sqlalchemy import select, insert
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import config
from app.database.postgres import Base, use_session
from app.utils.funcs import get_current_time_with_utc
from app.utils.password_manager import PasswordManager


class DateFieldMixin:
    """Class mixin adds create and update data fields to the database models"""
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                            default=get_current_time_with_utc())
    updated_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class Role(Base):
    """Database model, describes the table of roles in the database"""
    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint(f"role in {config.init.user_roles}"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"Role(id={self.id!r}, role={self.role!r})"

    def __repr__(self) -> str:
        return str(self)

    def dict(self) -> dict:
        return self.__dict__

    async def __is_role_exist(self) -> bool:
        """
        Method checks if the roles exist in the database

        Returns:
            true if there are roles in database table, false if not

        """
        stmt = select(self.__class__)
        async for session in use_session():
            role = await session.scalar(stmt)
            return bool(role)

    async def create_init_roles(self) -> None:
        """Method adds init roles to the database"""
        if not await self.__is_role_exist():
            user_roles = config.init.user_roles
            async for session in use_session():
                for role in user_roles:
                    stmt = insert(Role).values(role=role)
                    await session.execute(statement=stmt)
                    await session.commit()


class User(Base, DateFieldMixin):
    """Database model, describes the table of users in the database"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    birthday: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    main_photo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_user_activate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    activated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))
    role: Mapped["Role"] = relationship(back_populates="users")

    def __str__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, " \
               f"nickname={self.nickname!r}, email={self.email!r}, first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r},  role_id={self.role_id!r}, role={self.role!r}, " \
               f"birthday={self.birthday!r}, main_photo={self.main_photo!r})"

    def __repr__(self) -> str:
        return str(self)

    def dict(self) -> dict:
        return self.__dict__

    async def __is_user_exist(self) -> bool:
        """
        Method checks if the users exist in the database

        Returns:
            true if there are users in database table, false if not

        """
        stmt = select(self.__class__)
        async for session in use_session():
            user = await session.scalar(stmt)
            return bool(user)

    @staticmethod
    async def __get_role(role: str, raise_not_found=False) -> Role | None:
        """
        Method gets user's role and return this role from the database

        Args:
            role: role to select from database
            raise_not_found: if False - return None if user is not found in the database, return exception if True

        Returns:
            role from database

        """
        stmt = select(Role).where(Role.role == role)
        async for session in use_session():
            result = await session.scalar(stmt)
            if not result and raise_not_found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role} not found")

            return result

    async def creat_init_user(self) -> None:
        """Method insert init user to database"""
        if not await self.__is_user_exist():
            init_user_role = await self.__get_role(role=config.init.role, raise_not_found=True)
            hashed_password = PasswordManager(password=config.init.password).hash_password()
            stmt = insert(self.__class__).values(username=config.init.username, password=hashed_password,
                                                 nickname=config.init.nickname, email=config.init.email,
                                                 role_id=init_user_role.id, is_user_activate=True)
            async for session in use_session():
                await session.execute(statement=stmt)
                await session.commit()
