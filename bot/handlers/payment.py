"""
ProfitRadar MP — Заглушка оплаты (тестовый режим).
/pay — имитация покупки Pro тарифа.
"""
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.db.database import get_session
from bot.models.user import User

router = Router(name="payment")

class PaymentStates(StatesGroup):
    waiting_confirmation = State()

@router.message(Command("pay"))
async def cmd_pay(message: Message, state: FSMContext) -> None:
    """Команда /pay — показывает кнопку оплаты."""
    await state.clear()
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить 990 ₽", callback_data="pay_confirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="pay_cancel")],
        ]
    )
    
    await message.answer(
        "💎 <b>Подписка Pro — 990 ₽/мес</b>\n\n"
        "Что входит:\n"
        "• API WB/Ozon (автоподключение)\n"
        "• Ежедневный дайджест прибыли\n"
        "• Алерты при падении маржи\n"
        "• Автозагрузка данных по всем SKU\n"
        "• Рекомендации по оптимизации\n\n"
        "⚠️ <i>Это тестовый режим. Реальные деньги не списываются.</i>\n\n"
        "Нажмите кнопку ниже для оплаты:",
        reply_markup=keyboard,
    )
    await state.set_state(PaymentStates.waiting_confirmation)

@router.callback_query(F.data == "pay_confirm", PaymentStates.waiting_confirmation)
async def process_payment(callback: CallbackQuery, state: FSMContext) -> None:
    """Имитация процесса оплаты."""
    await callback.message.edit_text(
        " <b>Обработка платежа...</b>\n\n"
        "Пожалуйста, подождите 3 секунды.\n"
        "🔄 Подключение к платёжному шлюзу...\n"
        "🔄 Проверка карты...\n"
        "🔄 Подтверждение транзакции..."
    )
    await callback.answer()
    
    # Имитация задержки обработки платежа (3 секунды)
    await asyncio.sleep(3)
    
    # "Успешная оплата" — активируем Pro
    user_id = callback.from_user.id
    
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=callback.from_user.username)
            session.add(user)
        user.plan = "pro"
        await session.commit()
    
    await state.clear()
    
    await callback.message.edit_text(
        "✅ <b>Оплата прошла успешно!</b>\n\n"
        "🎉 Тариф Pro активирован.\n\n"
        "Теперь вам доступны:\n"
        "• Ежедневный дайджест прибыли\n"
        "• Алерты при падении маржи\n"
        "• Автозагрузка данных по всем SKU\n"
        "• Рекомендации по оптимизации\n\n"
        "Напишите /status чтобы проверить статус.\n"
        "Напишите /connect чтобы подключить API WB."
    )

@router.callback_query(F.data == "pay_cancel", PaymentStates.waiting_confirmation)
async def cancel_payment(callback: CallbackQuery, state: FSMContext) -> None:
    """Отмена оплаты."""
    await state.clear()
    await callback.message.edit_text("❌ Оплата отменена.")
    await callback.answer()