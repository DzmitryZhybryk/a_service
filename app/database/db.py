"""Module for storage database connects and session"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import base_config
from typing import AsyncGenerator

engine = create_async_engine(base_config.database_url, echo=base_config.postgres_echo)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def use_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Function creates database session

    Returns:
        database session

    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
