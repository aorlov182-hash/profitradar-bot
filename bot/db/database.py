from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from contextlib import asynccontextmanager
import asyncio

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
    Base.metadata.create_all(bind=engine)

class SyncToAsyncSession:
    """Обёртка, позволяющая использовать await с синхронной сессией."""
    def __init__(self, sync_session: Session):
        self._sync_session = sync_session

    async def get(self, entity, ident):
        return await asyncio.to_thread(self._sync_session.get, entity, ident)

    def add(self, instance):
        self._sync_session.add(instance)

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