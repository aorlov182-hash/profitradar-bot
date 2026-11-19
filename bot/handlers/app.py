from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="app")


@router.message(Command("app"))
async def app_command(message: Message):

    await message.answer(
        "📱 <b>Приложение ProfitRadar MP</b>\n\n"
        "✅ Оффлайн-калькулятор маржи\n"
        "✅ История расчетов\n"
        "✅ Работает без интернета\n\n"
        "🔗 <b>Репозиторий на GitHub:</b>\n"
        "https://github.com/aorlov182-hash/profitradar-bot\n\n"
        "💡 <b>Сайт:</b>\n"
        "https://aorlov182-hash.github.io/profitradar-site/"
    )