from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from app.config import settings  # if you're using a config class

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get an async session."""
    async with AsyncSessionLocal() as session:
        yield session