"""
ProfitRadar MP — Scheduler (APScheduler).
Запускает ежедневные дайджесты и проверки маржи.
"""
import logging
from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.db.database import get_session
from bot.models.user import User
from bot.handlers.digest import send_digest_to_user
from bot.handlers.alerts import send_alerts_to_user

logger = logging.getLogger(__name__)

async def daily_digest_job(bot) -> None:
    """Ежедневный дайджест для всех Pro-юзеров. 10:00 MSK."""
    logger.info("Running daily digest job...")
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.plan == "pro").where(User.digest_enabled == True)
        )
        users = result.scalars().all()
        logger.info(f"Found {len(users)} pro users for digest")
        for user in users:
            try:
                await send_digest_to_user(bot, user)
            except Exception as e:
                logger.error(f"Digest failed for user {user.id}: {e}")

async def margin_alert_job(bot) -> None:
    """Проверка маржи каждые 6 часов."""
    logger.info("Running margin alert job...")
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.plan == "pro").where(User.alerts_enabled == True)
        )
        users = result.scalars().all()
        for user in users:
            try:
                await send_alerts_to_user(bot, user)
            except Exception as e:
                logger.error(f"Alert check failed for user {user.id}: {e}")

def setup_scheduler(bot) -> AsyncIOScheduler:
    """Создаёт и настраивает планировщик."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        daily_digest_job,
        CronTrigger(hour=7, minute=0),  # 10:00 MSK (UTC+3)
        args=[bot],
        id="daily_digest",
        replace_existing=True,
    )
    scheduler.add_job(
        margin_alert_job,
        CronTrigger(hour="*/6"),
        args=[bot],
        id="margin_alert",
        replace_existing=True,
    )
    return scheduler