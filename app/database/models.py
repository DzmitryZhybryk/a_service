"""Module for storage database models"""
import datetime

from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import base_config
from app.database.postgres import Base
from app.utils.funcs import get_current_time_with_utc


class DateFieldMixin:
    """Class mixin adds create and update data fields to the database models"""
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                            default=get_current_time_with_utc())
    updated_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class Role(Base):
    """Database model, describes the table of roles in the database"""
    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint(f"role in {base_config.user_roles}"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"Role(id={self.id!r}, role={self.role!r})"

    def __repr__(self):
        return str(self)


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

    def __str__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, " \
               f"nickname={self.nickname!r}, email={self.email!r}, first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r},  role_id={self.role_id!r}, role={self.role!r}, " \
               f"birthday={self.birthday!r}, main_photo={self.main_photo!r})"

    def __repr__(self):
        return str(self)
