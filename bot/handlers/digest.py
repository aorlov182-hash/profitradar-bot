from aiogram import Router
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
            "✅ Алерты по марже\n"
            "✅ API маркетплейсов"
        )
        return

    await message.answer(
        "📬 Ваш PRO дайджест прибыли:\n\n"
        "Продажи: 0 ₽\n"
        "Прибыль: 0 ₽"
    )