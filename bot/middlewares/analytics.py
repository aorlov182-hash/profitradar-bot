"""
Middleware для сбора статистики действий пользователей.
"""
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import text
from bot.db.database import engine


class AnalyticsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Логируем действие пользователя
        if isinstance(event, Message):
            user_id = event.from_user.id
            action = f"command:{event.text}" if event.text and event.text.startswith('/') else "message"
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            action = f"callback:{event.data}"
        else:
            return await handler(event, data)
        
        # Записываем в БД
        try:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO stats (user_id, action) VALUES (:user_id, :action)"),
                    {"user_id": user_id, "action": action}
                )
                conn.commit()
        except Exception:
            pass  # Не ломаем бота, если статистика не записалась
        
        return await handler(event, data)