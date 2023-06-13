"""
Database configurations for whole the project.
"""
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine,
)

from models import Base

load_dotenv()

async_engine: AsyncEngine = create_async_engine(getenv("DSN"), echo=True)
async_db_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession,
)


async def init_db():
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await async_engine.dispose()
