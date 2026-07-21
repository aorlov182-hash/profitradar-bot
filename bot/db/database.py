from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from contextlib import asynccontextmanager
import asyncio
from pathlib import Path


class Base(DeclarativeBase):
    pass


engine = create_engine(
    "sqlite:///./data/bot.db",
    echo=False,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def init_db() -> None:
    """Синхронное создание таблиц."""
    from bot.models.user import User
    
    # Создаём папку data, если её нет
    Path("./data").mkdir(parents=True, exist_ok=True)
    
    # Создаём таблицы моделей (users)
    Base.metadata.create_all(bind=engine)
    
    # Создаём таблицу статистики вручную
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


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