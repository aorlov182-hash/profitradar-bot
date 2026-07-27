import os
from pathlib import Path
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.orm import DeclarativeBase
from bot.models.stat import Stat

# ==============================
# DATABASE CONFIGURATION
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

# Создаем папку data автоматически
DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


DEFAULT_DB_PATH = DATA_DIR / "bot.db"


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite+aiosqlite:///{DEFAULT_DB_PATH}"
)


# ==============================
# ENGINE
# ==============================

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)


# ==============================
# SESSION
# ==============================

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# ==============================
# BASE MODEL
# ==============================

class Base(DeclarativeBase):
    pass


# ==============================
# GET SESSION
# ==============================

@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session


# ==============================
# INIT DATABASE
# ==============================

async def init_db():
    """
    Создание таблиц базы данных
    """

    print(f"Database URL: {DATABASE_URL}")

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print("Database initialized")