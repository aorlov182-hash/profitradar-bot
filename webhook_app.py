import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Импортируем всё из вашего основного файла
from bot.config import settings
from bot.handlers import start, calculator, api_connect, digest, alerts, subscription, payment
from bot.middlewares.throttle import ThrottleMiddleware
from bot.db.database import init_db
from bot.services.scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")
logger = logging.getLogger(__name__)

# Переменные окружения от Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://profitradar-bot.onrender.com
PORT = int(os.getenv("PORT", 8000))     # Render сам передаст порт, по умолчанию 8000

def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        start.router, calculator.router, api_connect.router, 
        subscription.router, payment.router, digest.router, alerts.router,
    )

async def on_startup(bot: Bot) -> None:
    logger.info("Bot starting...")
    init_db()  # Инициализация SQLite
    logger.info("Database initialized")
    
    # Устанавливаем вебхук при запуске
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to: {WEBHOOK_URL}")
    
    # Запускаем планировщик (дайджесты и алерты)
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
    dp.message.middleware(ThrottleMiddleware(rate_limit=1.0))

    # Настраиваем aiohttp сервер для вебхука
    app = web.Application()
    
    # Обработчик вебхука (путь должен совпадать с тем, что мы укажем в set_webhook)
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    
    setup_application(app, dp, bot=bot)
    
    logger.info(f"Starting webhook server on port {PORT}...")
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())