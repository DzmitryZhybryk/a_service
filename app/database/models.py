import datetime

from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config import base_config
from app.database.db import Base
from app.utils.funcs import get_current_time_with_utc


class DateFieldMixin:
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_current_time_with_utc())
    updated_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class Role(Base):
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
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))
    role: Mapped["Role"] = relationship(back_populates="users")
