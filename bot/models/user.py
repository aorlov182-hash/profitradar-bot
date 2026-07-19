"""
ProfitRadar MP — User model.
Хранит Telegram ID, тарифный план, зашифрованные API-ключи.
"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from bot.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Telegram user_id
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    plan: Mapped[str] = mapped_column(String(10), default="free")  # free | pro
    wb_api_key_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ozon_api_key_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)
    digest_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    alerts_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_digest_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)