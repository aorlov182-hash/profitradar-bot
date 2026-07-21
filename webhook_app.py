import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import settings
from bot.handlers import start, calculator, api_connect, digest, alerts, subscription, payment, admin
from bot.middlewares.throttle import ThrottleMiddleware
from bot.middlewares.analytics import AnalyticsMiddleware
from bot.db.database import init_db
from bot.services.scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 10000))

def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        start.router,
        calculator.router,
        api_connect.router,
        subscription.router,
        payment.router,
        admin.router,  # <-- ДОБАВЛЕНО
        digest.router,
        alerts.router,
    )

async def on_startup(bot: Bot) -> None:
    logger.info("Bot starting...")
    init_db()
    logger.info("Database initialized")
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to: {WEBHOOK_URL}")
    scheduler = setup_scheduler(bot)
    scheduler.start()

async def on_shutdown(bot: Bot) -> None:
    logger.info("Bot shutting down...")
    await bot.delete_webhook()
    logger.info("Webhook deleted")

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    setup_routers(dp)
    
    # Подключаем middleware (ДОБАВЛЕНО)
    dp.message.middleware(ThrottleMiddleware(rate_limit=1.0))
    dp.message.middleware(AnalyticsMiddleware())
    dp.callback_query.middleware(AnalyticsMiddleware())

    app = web.Application()
    
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    
    setup_application(app, dp, bot=bot)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    
    logger.info(f"Server started on port {PORT}")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())