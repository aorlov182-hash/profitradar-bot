import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings

from bot.handlers import (
    start,
    calculator,
    compare,
    api_connect,
    digest,
    alerts,
    subscription,
    payment,
    admin,
    app
)

from bot.middlewares.throttle import ThrottleMiddleware
from bot.middlewares.analytics import AnalyticsMiddleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def setup_routers(dp: Dispatcher):

    dp.include_routers(
        start.router,
        calculator.router,
        compare.router,
        api_connect.router,
        subscription.router,
        payment.router,
        admin.router,
        digest.router,
        alerts.router,
        app.router,
    )


async def main():

    logger.info("🚀 Запуск ProfitRadar MP")


    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )


    dp = Dispatcher()


    setup_routers(dp)


    dp.message.middleware(
        ThrottleMiddleware(rate_limit=1.0)
    )

    dp.message.middleware(
        AnalyticsMiddleware()
    )

    dp.callback_query.middleware(
        AnalyticsMiddleware()
    )


    # Удаляем webhook перед polling
    await bot.delete_webhook(drop_pending_updates=True)


    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        logger.info("Бот остановлен")



if __name__ == "__main__":
    asyncio.run(main())