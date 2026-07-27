"""
Админ-команды для просмотра статистики.
"""

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy import text

from bot.db.database import engine
from bot.config import settings

logger = logging.getLogger(__name__)

router = Router(name="admin")


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    """Показывает статистику бота (только для администратора)."""

    user_id = message.from_user.id

    logger.info(f"Получена команда /stats от пользователя ID: {user_id}")

    try:
        admin_id = int(settings.admin_user_id)

    except (ValueError, TypeError):
        logger.error("ADMIN_USER_ID указан неверно")
        await message.answer("Ошибка конфигурации администратора.")
        return

    if user_id != admin_id:
        logger.warning(
            f"Отказано в доступе. user={user_id}, admin={admin_id}"
        )
        await message.answer(
            "Эта команда доступна только администратору."
        )
        return

    logger.info("Запрашиваем статистику...")

    try:

        async with engine.connect() as conn:

            # Всего пользователей
            result = await conn.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM stats
                    """
                )
            )
            total_users = result.scalar() or 0

            # Активные сегодня
            result = await conn.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM stats
                    WHERE created_at >= date('now','start of day')
                    """
                )
            )
            active_today = result.scalar() or 0

            # Активные за неделю
            result = await conn.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM stats
                    WHERE created_at >= date('now','-7 day')
                    """
                )
            )
            active_week = result.scalar() or 0

            # Ожидание Pro
            result = await conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM stats
                    WHERE action='callback:notify_pro'
                    """
                )
            )
            waitlist_count = result.scalar() or 0

            # ТОП команд
            result = await conn.execute(
                text(
                    """
                    SELECT action,
                           COUNT(*) AS count
                    FROM stats
                    WHERE action LIKE 'command:%'
                    GROUP BY action
                    ORDER BY count DESC
                    LIMIT 5
                    """
                )
            )

            top_commands = result.fetchall()

        stats_text = (
            "📊 <b>Статистика ProfitRadar</b>\n\n"
            f"👥 Всего пользователей: <b>{total_users}</b>\n"
            f"📅 Активных сегодня: <b>{active_today}</b>\n"
            f"📆 Активных за неделю: <b>{active_week}</b>\n\n"
            f"🔔 В списке ожидания Pro: <b>{waitlist_count}</b>\n\n"
            "<b>Топ команд:</b>\n"
        )

        if top_commands:

            for action, count in top_commands:

                command = action.replace(
                    "command:",
                    "/"
                )

                stats_text += (
                    f"• {command} — {count}\n"
                )

        else:

            stats_text += "Пока нет данных."

        await message.answer(stats_text)

        logger.info("Статистика успешно отправлена.")

    except Exception as e:

        logger.exception(e)

        await message.answer(
            "Произошла ошибка при чтении статистики."
        )