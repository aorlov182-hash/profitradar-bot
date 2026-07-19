"""
ProfitRadar MP — Управление подпиской Pro.
/pro — информация о тарифах и активация.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="subscription")

@router.message(Command("pro"))
async def cmd_pro(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Купить Pro за 990 ₽", callback_data="pay_start")],
        ]
    )
    
    await message.answer(
        "💎 <b>Тарифы ProfitRadar</b>\n\n"
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
        "Нажмите кнопку ниже для покупки Pro:",
        reply_markup=keyboard,
    )

@router.callback_query(lambda c: c.data == "pay_start")
async def callback_pay_start(callback: CallbackQuery) -> None:
    """Перенаправление на команду /pay при нажатии кнопки в /pro."""
    await callback.message.answer(
        "💎 <b>Подписка Pro — 990 ₽/мес</b>\n\n"
        "Что входит:\n"
        "• API WB/Ozon (автоподключение)\n"
        "• Ежедневный дайджест прибыли\n"
        "• Алерты при падении маржи\n"
        "• Автозагрузка данных по всем SKU\n"
        "• Рекомендации по оптимизации\n\n"
        "⚠️ <i>Это тестовый режим. Реальные деньги не списываются.</i>\n\n"
        "Напишите /pay для оплаты.",
    )
    await callback.answer()