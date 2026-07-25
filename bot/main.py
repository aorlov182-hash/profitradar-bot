import sys
from pathlib import Path

# Добавляем корневую папку проекта в путь поиска модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.handlers import (
    start,
    calculator,
    api_connect,
    digest,
    alerts,
    subscription,
    payment,
    admin,
    compare,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Создание бота и диспетчера
bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключение роутеров
dp.include_router(start.router)
dp.include_router(calculator.router)
dp.include_router(api_connect.router)
dp.include_router(digest.router)
dp.include_router(alerts.router)
dp.include_router(subscription.router)
dp.include_router(payment.router)
dp.include_router(admin.router)
dp.include_router(compare.router)


# Команда /app
@dp.message(Command("app"))
async def app_command(message: types.Message):
    await message.answer(
        "📱 <b>Скачать приложение ProfitRadar MP</b>\n\n"
        "✅ Оффлайн-калькулятор маржи\n"
        "✅ История расчетов\n"
        "✅ Работает без интернета\n\n"
        "🔗 Скачать APK:\n"
        "https://github.com/aorlov182-hash/profitradar-bot/releases/download/v1.0.0/ProfitRadar.apk\n\n"
        "💡 Инструкция:\n"
        "https://aorlov182-hash.github.io/profitradar-site/",
        disable_web_page_preview=False,
    )


async def main():
    logger.info("Запуск бота...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())