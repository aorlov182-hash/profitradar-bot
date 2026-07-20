"""
ProfitRadar MP — Управление подпиской Pro.
/pro — информация о тарифах и кнопка "Скоро будет".
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="subscription")

@router.message(Command("pro"))
async def cmd_pro(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Напомнить о запуске", callback_data="notify_pro")],
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
        " <b>Pro тариф скоро будет доступен!</b>\n\n"
        "Нажмите кнопку ниже, чтобы мы напомнили вам о запуске.",
        reply_markup=keyboard,
    )

@router.callback_query(lambda c: c.data == "notify_pro")
async def callback_notify_pro(callback) -> None:
    """Пользователь хочет быть уведомлен о запуске Pro."""
    await callback.message.edit_text(
        "✅ <b>Отлично!</b>\n\n"
        "Мы записали вас в список ожидания.\n"
        "Как только Pro тариф будет запущен, вы получите уведомление первым!\n\n"
        "А пока пользуйтесь бесплатным калькулятором — он уже работает 📊",
    )
    await callback.answer("Вы записаны в список ожидания!")