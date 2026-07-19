"""
ProfitRadar MP — Управление подпиской Pro.
/pro — информация о тарифах и активация.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router(name="subscription")

@router.message(Command("pro"))
async def cmd_pro(message: Message) -> None:
    await message.answer(
        "<b>💎 Тарифы ProfitRadar</b>\n\n"
        "<b>Free (бесплатно)</b>\n"
        "• Калькулятор маржи без лимитов\n"
        "• Ручной ввод данных\n"
        "• Мгновенный расчёт\n\n"
        "<b>Pro — 990 ₽/мес</b>\n"
        "• API WB/Ozon (автоподключение)\n"
        "• Ежедневный дайджест прибыли\n"
        "• Алерты при падении маржи\n"
        "• Автозагрузка данных по всем SKU\n"
        "• Рекомендации по оптимизации\n\n"
        "Чтобы подключить Pro — напиши /connect\n"
        "и отправь API-ключ из кабинета WB.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔗 Подключить API")],
                [KeyboardButton(text="❌ Отмена")],
            ],
            resize_keyboard=True,
        ),
    )