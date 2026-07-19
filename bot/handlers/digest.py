"""
ProfitRadar MP — Ежедневный дайджест прибыли (Pro).
Присылает утром сводку по марже.
"""
import logging
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from bot.models.user import User

logger = logging.getLogger(__name__)
router = Router(name="digest")

async def send_digest_to_user(bot, user: User) -> None:
    """Отправить дайджест пользователю."""
    try:
        text = (
            f"📬 <b>Ежедневный дайджест ProfitRadar</b>\n\n"
            f"Привет, {user.username or 'селлер'}!\n\n"
            f"Сегодня {datetime.now().strftime('%d.%m.%Y')}\n\n"
            f"⚠ Это демо-дайджест. "
            f"Подключи API WB через /connect, чтобы получать "
            f"реальные данные по твоему магазину.\n\n"
            f"В следующей версии:\n"
            f"• Выручка за вчера\n"
            f"• Расходы по категориям\n"
            f"• Топ-3 прибыльных SKU\n"
            f"• Топ-3 убыточных SKU\n"
            f"• Изменение маржи за неделю"
        )
        await bot.send_message(chat_id=user.id, text=text)
    except Exception as e:
        logger.error(f"Failed to send digest to user {user.id}: {e}")