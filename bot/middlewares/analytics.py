from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import text

from bot.db.database import async_session


class AnalyticsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        if isinstance(event, Message):
            user_id = event.from_user.id
            action = (
                f"command:{event.text}"
                if event.text and event.text.startswith("/")
                else "message"
            )

        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            action = f"callback:{event.data}"

        else:
            return await handler(event, data)

        try:
            async with async_session() as session:
                await session.execute(
                    text(
                        """
                        INSERT INTO stats (user_id, action)
                        VALUES (:user_id, :action)
                        """
                    ),
                    {
                        "user_id": user_id,
                        "action": action,
                    },
                )
                await session.commit()

        except Exception as e:
            print(f"Analytics error: {e}")

        return await handler(event, data)