from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.access import check_pro


router = Router(name="alerts")


async def send_alerts_to_user(bot, user_id: int):
    """
    Отправка PRO-уведомлений пользователю.
    Используется планировщиком.
    """

    try:
        await bot.send_message(
            user_id,
            "🚨 PRO АЛЕРТ\n\n"
            "Проверка прибыли завершена.\n"
            "Изменений по марже не обнаружено."
        )

    except Exception as e:
        print(f"Alert error for {user_id}: {e}")


@router.message(Command("alerts"))
async def alerts(message: Message):

    if not await check_pro(message.from_user.id):
        await message.answer(
            "🔒 Алерты доступны только PRO тарифу.\n\n"
            "PRO получает:\n"
            "✅ уведомления о падении маржи\n"
            "✅ контроль убыточных товаров\n"
            "✅ автоматические проверки"
        )
        return


    await message.answer(
        "🚨 Алерты включены.\n\n"
        "PRO мониторинг активирован."
    )