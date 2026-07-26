from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.access import check_pro


router = Router(name="api_connect")


@router.message(Command("connect"))
async def connect(message: Message):

    if not await check_pro(message.from_user.id):
        await message.answer(
            "🔒 Подключение API WB/Ozon доступно только PRO.\n\n"
            "PRO тариф:\n"
            "990 ₽/месяц"
        )
        return


    await message.answer(
        "🔗 API подключение доступно."
    )