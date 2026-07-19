"""
ProfitRadar MP — Throttle middleware (антиспам).
Ограничивает частоту сообщений от одного пользователя.
"""
from typing import Any, Awaitable, Callable, Dict
import time
from aiogram import BaseMiddleware
from aiogram.types import Message

class ThrottleMiddleware(BaseMiddleware):
    """Antiflood: 1 сообщение в секунду на пользователя."""
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.user_last_msg: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        now = time.time()
        last = self.user_last_msg.get(user_id, 0)
        
        if now - last < self.rate_limit:
            return  # Игнорируем слишком частые сообщения
        
        self.user_last_msg[user_id] = now
        return await handler(event, data)