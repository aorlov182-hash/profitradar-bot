from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="app")

@router.message(Command("app"))
async def app_command(message: Message):
    await message.answer(
        "📱 Скачать приложение ProfitRadar MP\n\n"
        "https://github.com/aorlov182-hash/profitradar-bot/releases/download/v1.0.0/ProfitRadar.apk"
    )