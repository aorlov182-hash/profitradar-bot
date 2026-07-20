"""
ProfitRadar MP — Заглушка оплаты (Pro скоро будет).
/pay — показывает сообщение о скором запуске.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="payment")

@router.message(Command("pay"))
async def cmd_pay(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Напомнить о запуске", callback_data="notify_pro")],
            [InlineKeyboardButton(text="📊 Попробовать калькулятор", callback_data="try_calc")],
        ]
    )
    
    await message.answer(
        " <b>Pro тариф скоро будет доступен!</b>\n\n"
        "Мы активно работаем над подключением платежей.\n\n"
        "Что входит в Pro:\n"
        "• API WB/Ozon (автоподключение)\n"
        "• Ежедневный дайджест прибыли\n"
        "• Алерты при падении маржи\n"
        "• Автозагрузка данных по всем SKU\n"
        "• Рекомендации по оптимизации\n\n"
        "💰 Стоимость: <b>990 ₽/мес</b>\n\n"
        "Нажмите кнопку, чтобы мы напомнили вам о запуске.\n"
        "А пока попробуйте бесплатный калькулятор! 👇",
        reply_markup=keyboard,
    )

@router.callback_query(lambda c: c.data == "notify_pro")
async def callback_notify_pro(callback) -> None:
    """Пользователь хочет быть уведомлен о запуске Pro."""
    await callback.message.edit_text(
        "✅ <b>Отлично!</b>\n\n"
        "Мы записали вас в список ожидания.\n"
        "Как только Pro тариф будет запущен, вы получите уведомление первым!\n\n"
        "А пока пользуйтесь бесплатным калькулятором — он уже работает ",
    )
    await callback.answer("Вы записаны в список ожидания!")

@router.callback_query(lambda c: c.data == "try_calc")
async def callback_try_calc(callback) -> None:
    """Перенаправление на калькулятор."""
    await callback.message.answer(
        "📊 <b>Калькулятор маржи</b>\n\n"
        "Напишите /calc, чтобы рассчитать маржу для вашего товара.",
    )
    await callback.answer()