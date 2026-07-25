import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь поиска модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# Исправленные импорты
from bot.config import settings
from bot.handlers import start, calculator, api_connect, digest, alerts, subscription, payment, admin, compare

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание бота и диспетчера
bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация хендлеров
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
    await message.reply(
        "📱 **Скачать приложение ProfitRadar MP**\n\n"
        "✅ Оффлайн-калькулятор маржи\n"
        "✅ История расчетов\n"
        "✅ Работает без интернета\n\n"
        "🔗 **Скачать APK (бесплатно, 49 МБ):**\n"
        "https://github.com/aorlov182-hash/profitradar-bot/releases/download/v1.0.0/ProfitRadar.apk\n\n"
        "💡 **Сайт с инструкциями:**\n"
        "https://aorlov182-hash.github.io/profitradar-site/",
        parse_mode="markdown",
        disable_web_page_preview=False
    )

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = [
        [InlineKeyboardButton("🌐 Открыть сайт", url="https://aorlov182-hash.github.io/profitradar-site/")],
        [InlineKeyboardButton("📱 Скачать приложение", callback_data="download_app")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.reply(
        " Добро пожаловать в **ProfitRadar MP**!\n\n"
        "Я помогу вам рассчитать маржу и прибыль от продаж на маркетплейсах.\n\n"
        "Выберите действие:",
        reply_markup=reply_markup,
        parse_mode="markdown"
    )

async def main():
    """Основная функция запуска бота"""
    logger.info("Запуск бота...")
    
    try:
        # Запуск бота методом polling (для локальной разработки)
        await dp.start_polling(bot)
    finally:
        # Корректное завершение работы
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())