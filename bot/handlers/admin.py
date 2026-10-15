"""
Админ-команды для просмотра статистики.
SQL-запросы универсальны: работают и на SQLite, и на PostgreSQL.
"""

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text

from bot.config import settings
from bot.db.database import async_session, switch_to_sqlite, get_session_maker

logger = logging.getLogger(__name__)

router = Router(name="admin")


@router.message(Command("stats"))
async def cmd_stats(message: Message):

    user_id = message.from_user.id

    logger.info(f"Получена команда /stats от пользователя ID: {user_id}")

    try:
        admin_id = int(settings.admin_user_id)

    except (ValueError, TypeError):
        await message.answer("Ошибка конфигурации ADMIN_USER_ID")
        return

    if user_id != admin_id:
        await message.answer("Эта команда доступна только администратору.")
        return

    async def _fetch_stats(session):
        total_users = (
            await session.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM stats
                    """
                )
            )
        ).scalar() or 0

        # Универсальный фильтр "за сегодня":
        # - PostgreSQL: CURRENT_DATE
        # - SQLite: date('now')
        active_today = (
            await session.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM stats
                    WHERE created_at >= CURRENT_DATE
                    """
                )
            )
        ).scalar() or 0

        # Универсальный фильтр "за 7 дней":
        # - PostgreSQL: CURRENT_DATE - INTERVAL '7 days'
        # - SQLite: date('now', '-7 days')
        active_week = (
            await session.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT user_id)
                    FROM stats
                    WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
                    """
                )
            )
        ).scalar() or 0

        top_commands = (
            await session.execute(
                text(
                    """
                    SELECT action, COUNT(*) AS count
                    FROM stats
                    WHERE action LIKE 'command:%'
                    GROUP BY action
                    ORDER BY count DESC
                    LIMIT 5
                    """
                )
            )
        ).fetchall()

        waitlist_count = (
            await session.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM stats
                    WHERE action='callback:notify_pro'
                    """
                )
            )
        ).scalar() or 0

        return total_users, active_today, active_week, top_commands, waitlist_count

    try:

        async with async_session() as session:
            total_users, active_today, active_week, top_commands, waitlist_count = await _fetch_stats(session)

    except Exception as e:
        logger.warning("Первая попытка чтения статистики не удалась: %s", e)
        # Если PostgreSQL недоступен — переключаемся на SQLite и пробуем ещё раз.
        try:
            switch_to_sqlite(str(e))
            async with get_session_maker()() as session:
                total_users, active_today, active_week, top_commands, waitlist_count = await _fetch_stats(session)
        except Exception as e2:
            logger.exception("Ошибка чтения статистики после переключения на SQLite: %s", e2)
            await message.answer(
                "Ошибка при чтении статистики. База данных недоступна.\n"
                "Если вы на Render — проверьте переменную DATABASE_URL "
                "(удалите её, если PostgreSQL не нужен — будет использоваться SQLite)."
            )
            return

    stats_text = (
        "📊 <b>Статистика ProfitRadar</b>\n\n"
        f"👥 Пользователей: <b>{total_users}</b>\n"
        f"📅 Сегодня: <b>{active_today}</b>\n"
        f"📆 За неделю: <b>{active_week}</b>\n\n"
        f"💎 Ждут Pro: <b>{waitlist_count}</b>\n\n"
        "<b>🔥 Топ команд</b>\n"
    )

    if top_commands:
        for action, count in top_commands:
            command = action.replace("command:", "")
            stats_text += f"• {command} — {count}\n"
    else:
        stats_text += "Пока нет данных."

    await message.answer(stats_text)
