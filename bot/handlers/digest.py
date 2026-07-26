from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.access import check_pro


router = Router(name="digest")


@router.message(Command("digest"))
async def digest(message: Message):

    if not await check_pro(message.from_user.id):
        await message.answer(
            "🔒 Дайджест прибыли доступен только PRO пользователям.\n\n"
            "PRO: 990 ₽/месяц\n\n"
            "В PRO входит:\n"
            "✅ Дайджест прибыли\n"
            "✅ Алерты по падению маржи\n"
            "✅ API маркетплейсов"
        )
        return

    await message.answer(
        "📬 Ваш PRO дайджест прибыли:\n\n"
        "Продажи: 0 ₽\n"
        "Прибыль: 0 ₽\n\n"
        "Автоматический расчет будет доступен после подключения API."
    )


async def send_digest_to_user(bot: Bot, user_id: int):
    """
    Отправка ежедневного PRO дайджеста пользователю.
    Используется планировщиком APScheduler.
    """

    await bot.send_message(
        user_id,
        "📬 Ваш ежедневный PRO дайджест прибыли:\n\n"
        "📦 Продажи: 0 ₽\n"
        "💰 Прибыль: 0 ₽\n\n"
        "ProfitRadar MP"
    )