from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="app")


@router.message(Command("app"))
async def app_command(message: Message):

    await message.answer(
        "📱 <b>Скачать приложение ProfitRadar MP</b>\n\n"
        "✅ Оффлайн-калькулятор маржи\n"
        "✅ История расчетов\n"
        "✅ Работает без интернета\n\n"
        "🔗 <b>Скачать APK (49 МБ):</b>\n"
        "https://github.com/aorlov182-hash/profitradar-bot/releases/download/v1.0.0/ProfitRadar.apk\n\n"
        "💡 <b>Сайт с инструкциями:</b>\n"
        "https://aorlov182-hash.github.io/profitradar-site/",
        disable_web_page_preview=False
    )