from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings

engine = create_async_engine(
    url=str(settings.database.url), echo=True, future=True
)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session_cm():
    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        yield session
    finally:
        await session_gen.aclose()
