"""
ProfitRadar MP — Алерты при падении маржи (Pro).
Проверяет маржу каждые 6 часов и шлёт уведомление.
"""
import logging
from aiogram import Router
from bot.models.user import User

logger = logging.getLogger(__name__)
router = Router(name="alerts")

async def send_alerts_to_user(bot, user: User) -> None:
    """Проверить маржу и отправить алерт если нужно."""
    try:
        # Заглушка: в реальной версии здесь будет запрос к API WB
        # и анализ маржи по всем SKU
        text = (
            f" <b>Алерт ProfitRadar</b>\n\n"
            f"Привет, {user.username or 'селлер'}!\n\n"
            f"⚠ Это демо-алерт. "
            f"Подключи API WB через /connect, чтобы получать "
            f"реальные уведомления при падении маржи.\n\n"
            f"В следующей версии:\n"
            f"• SKU с маржой ниже порога\n"
            f"• Резкий рост расходов\n"
            f"• Аномальные возвраты\n"
            f"• Рекомендации по действиям"
        )
        await bot.send_message(chat_id=user.id, text=text)
    except Exception as e:
        logger.error(f"Failed to send alerts to user {user.id}: {e}")