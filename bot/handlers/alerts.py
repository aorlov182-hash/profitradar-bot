from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.access import check_pro


router = Router(name="alerts")


@router.message(Command("alerts"))
async def alerts(message: Message):

    if not await check_pro(message.from_user.id):
        await message.answer(
            "🚨 Алерты доступны только PRO тарифу.\n\n"
            "PRO получает уведомления:\n"
            "• падение маржи\n"
            "• убыточные товары\n"
            "• контроль прибыли"
        )
        return

    await message.answer(
        "🚨 Алерты включены."
    )