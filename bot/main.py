import asyncio
import logging
import sys
from pathlib import Path

# Корень проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
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
    compare
)


# ==========================
# Логирование
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================
# Бот
# ==========================

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


# ==========================
# Dispatcher
# ==========================

dp = Dispatcher(
    storage=MemoryStorage()
)


# ==========================
# Подключение handlers
# ==========================

dp.include_router(start.router)
dp.include_router(calculator.router)
dp.include_router(api_connect.router)
dp.include_router(digest.router)
dp.include_router(alerts.router)
dp.include_router(subscription.router)
dp.include_router(payment.router)
dp.include_router(admin.router)
dp.include_router(compare.router)


# ==========================
# Команда /app
# ==========================

@dp.message(Command("app"))
async def app_command(message: types.Message):

    await message.answer(
        "📱 <b>Скачать приложение ProfitRadar MP</b>\n\n"
        "✅ Оффлайн-калькулятор маржи\n"
        "✅ История расчетов\n"
        "✅ Работает без интернета\n\n"
        "🔗 <b>Скачать APK:</b>\n"
        "https://github.com/aorlov182-hash/profitradar-bot/releases/download/v1.0.0/ProfitRadar.apk\n\n"
        "💡 <b>Инструкция:</b>\n"
        "https://aorlov182-hash.github.io/profitradar-site/",
        disable_web_page_preview=False
    )


# ==========================
# Запуск
# ==========================

async def main():

    logger.info("🚀 Запуск ProfitRadar MP")

    try:

        # Убираем webhook перед локальным polling
        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)


    except Exception as e:

        logger.exception(
            f"Ошибка запуска бота: {e}"
        )


    finally:

        await bot.session.close()

        logger.info(
            "Бот остановлен"
        )


# ==========================

if __name__ == "__main__":

    asyncio.run(main())