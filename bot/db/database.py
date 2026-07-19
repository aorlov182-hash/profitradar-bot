from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from bot.config import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(
    "sqlite:///./data/bot.db",
    echo=False,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

def init_db() -> None:
    from bot.models.user import User
    Base.metadata.create_all(bind=engine)

def get_session() -> Session:
    return SessionLocal()