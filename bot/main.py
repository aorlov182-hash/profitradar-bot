"""
ProfitRadar MP Bot — точка входа.
Запуск: python -m bot.main
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from bot.config import settings
from bot.handlers import start, calculator, api_connect, digest, alerts, subscription, payment, admin
from bot.middlewares.throttle import ThrottleMiddleware
from bot.middlewares.analytics import AnalyticsMiddleware
from bot.db.database import init_db
from bot.services.scheduler import setup_scheduler

logger = logging.getLogger(__name__)


def setup_routers(dp: Dispatcher) -> None:
    """Подключаем все роутеры."""
    dp.include_routers(
        start.router,
        calculator.router,
        api_connect.router,
        subscription.router,
        payment.router,
        admin.router,
        digest.router,
        alerts.router,
    )


def setup_middlewares(dp: Dispatcher) -> None:
    """Подключаем middleware."""
    dp.message.middleware(ThrottleMiddleware(rate_limit=1.0))
    dp.message.middleware(AnalyticsMiddleware())
    dp.callback_query.middleware(AnalyticsMiddleware())


async def on_startup(bot: Bot) -> None:
    """Действия при старте."""
    logger.info("Bot starting...")
    init_db()
    logger.info("Database initialized")
    # Уведомление админу
    try:
        await bot.send_message(
            chat_id=settings.admin_user_id,
            text="✅ Бот запущен"
        )
    except Exception:
        pass


async def on_shutdown(bot: Bot) -> None:
    """Действия при остановке."""
    logger.info("Bot shutting down...")
    try:
        await bot.send_message(
            chat_id=settings.admin_user_id,
            text=" Бот остановлен"
        )
    except Exception:
        pass


async def main() -> None:
    """Главная функция."""
    # Логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Бот
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # Диспетчер
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # Подключение
    setup_routers(dp)
    setup_middlewares(dp)
    # Планировщик (дайджесты, алерты)
    scheduler = setup_scheduler(bot)
    scheduler.start()
    # Запуск polling
    try:
        logger.info("Starting polling...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())