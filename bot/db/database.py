from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from contextlib import asynccontextmanager
import asyncio
import os
from pathlib import Path

# Универсальный URL базы.
# - Если задана переменная окружения DATABASE_URL/DB_URL (для Render/Postgres) —
#   используем её.
# - Иначе откатываемся на локальный SQLite (для разработки).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    os.getenv("DB_URL", "sqlite:///./data/bot.db")
)

_is_sqlite = DATABASE_URL.startswith("sqlite")


class Base(DeclarativeBase):
    pass


# Для SQLite нужен параметр check_same_thread=False,
# для PostgreSQL он не нужен.
_connect_args = {"check_same_thread": False} if _is_sqlite else {}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args=_connect_args,
)

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def init_db() -> None:
    """Синхронное создание таблиц."""
    # Импортируем модели, чтобы зарегистрировать их в Base.metadata
    # (это гарантирует создание таблиц users и т.д.).
    import bot.models.user  # noqa: F401

    # Создаём папку data только для SQLite
    if _is_sqlite:
        Path("./data").mkdir(parents=True, exist_ok=True)

    # Создаём таблицы моделей (users)
    Base.metadata.create_all(bind=engine)

    # Создаём таблицу статистики вручную (универсально для SQLite и Postgres)
    create_stats_table()


def create_stats_table() -> None:
    """Создаёт таблицу stats, если её нет (SQLite и PostgreSQL)."""
    with engine.begin() as conn:
        if _is_sqlite:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
        else:
            # PostgreSQL: SERIAL для id, TIMESTAMP WITHOUT TIME ZONE
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS stats (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    action TEXT,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
                )
            """))


class SyncToAsyncSession:
    """Обёртка, позволяющая использовать await с синхронной сессией."""
    def __init__(self, sync_session: Session):
        self._sync_session = sync_session

    async def get(self, entity, ident):
        return await asyncio.to_thread(self._sync_session.get, entity, ident)

    def add(self, instance):
        self._sync_session.add(instance)

    async def execute(self, statement, params=None):
        """Выполняет SQL-запрос (например, select) в отдельном потоке."""
        def _run_execute():
            return self._sync_session.execute(statement, params)
        return await asyncio.to_thread(_run_execute)

    async def commit(self):
        await asyncio.to_thread(self._sync_session.commit)

    async def close(self):
        await asyncio.to_thread(self._sync_session.close)


@asynccontextmanager
async def get_session():
    sync_session = SessionLocal()
    try:
        yield SyncToAsyncSession(sync_session)
    finally:
        await asyncio.to_thread(sync_session.close)
