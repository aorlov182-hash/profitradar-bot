import logging
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)


# ==============================
# BASE MODEL
# ==============================

class Base(DeclarativeBase):
    pass


# ==============================
# DATABASE CONFIGURATION
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DEFAULT_DB_PATH = DATA_DIR / "bot.db"

SQLITE_URL = f"sqlite+aiosqlite:///{DEFAULT_DB_PATH}"


def _normalize_db_url(raw: str) -> str:
    """Приводит DATABASE_URL к виду, понятному SQLAlchemy-async.

    - пустая строка -> SQLite (как было изначально);
    - `postgresql://...` -> `postgresql+asyncpg://...`.
    """
    raw = (raw or "").strip()
    if not raw:
        return SQLITE_URL
    if raw.startswith("postgresql://"):
        raw = "postgresql+asyncpg://" + raw[len("postgresql://"):]
    return raw


def _mask_db_url(url: str) -> str:
    """Маскирует пароль в строке подключения (не светим его в логах)."""
    return re.sub(r"://([^:/@]+):([^@/]+)@", r"://\1:***@", url)


DATABASE_URL = _normalize_db_url(os.getenv("DATABASE_URL", ""))


# ==============================
# ENGINE (ленивый, с fallback на SQLite)
# ==============================

_engine = None
_session_maker = None


def get_engine():
    global _engine
    if _engine is None:
        logger.info("DB engine: %s", _mask_db_url(DATABASE_URL))
        _engine = create_async_engine(DATABASE_URL, echo=False)
    return _engine


def get_session_maker():
    global _session_maker
    if _session_maker is None:
        _session_maker = async_sessionmaker(
            get_engine(),
            expire_on_commit=False,
            class_=AsyncSession,
        )
    return _session_maker


def switch_to_sqlite(reason: str) -> None:
    """Временный fallback на локальную SQLite, если PostgreSQL недоступен."""
    global _engine, _session_maker
    logger.warning("PostgreSQL недоступен (%s). Переключаюсь на SQLite.", reason)
    # Старый engine не диспозим здесь: AsyncEngine.dispose() — корутина,
    # а при неудачном первом коннекте пул уже ни на что не ссылается.
    _engine = create_async_engine(SQLITE_URL, echo=False)
    _session_maker = None


class _LazySessionFactory:
    """Совместим с прежним `async_session()`: берёт актуальный engine."""

    def __call__(self, **kw):
        return get_session_maker()(**kw)


async_session = _LazySessionFactory()


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
    # ВАЖНО:
    # импортируем модели здесь, после создания Base
    from bot.models.user import User  # noqa: F401
    from bot.models.stat import Stat  # noqa: F401

    # Пробуем инициализировать БД. Если PostgreSQL недоступен (DNS,
    # соединение, пароль — любая ошибка), переключаемся на локальную SQLite
    # и продолжаем работу без остановки бота.
    try:
        async with get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized (URL: %s)", _mask_db_url(DATABASE_URL))
    except Exception as e:
        logger.warning("PostgreSQL недоступен (%s). Переключаюсь на SQLite.", e)
        switch_to_sqlite(str(e))
        try:
            async with get_engine().begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database re-initialized on SQLite (temporary fallback)")
        except Exception as e2:
            logger.error("Не удалось инициализировать даже SQLite: %s", e2)
            raise
