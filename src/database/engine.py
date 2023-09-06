"""Database-engine functions"""
from sqlalchemy import MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)


def construct_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(
        url,
        echo=False,
        # encoding='utf-8',
        pool_pre_ping=True,
    )


async def proceed_schemas(
        engine: AsyncEngine,
        metadata: MetaData,
) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
