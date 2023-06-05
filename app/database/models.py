from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base


# class DateFieldMixin:
#     created_date: datetime = ormar.DateTime(default=get_current_time_with_utc(), timezone=True)
#     updated_date: datetime = ormar.DateTime(nullable=True, default=None, timezone=True)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
