from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.engine import URL

from app.core.config import config
from app.infra.sqlAlchemy.config.Base import Base

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=config.db.user,
    password=config.db.password,
    host=config.db.host,
    port=5432,
    database=config.db.database,
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    print("Init DB called")

    from app.infra.sqlAlchemy.model.order_model import OrderModel
    print(Base.metadata.tables)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables synchronized.")