"""
ProfitRadar MP — Подключение API WB.
/connect — ввод ключа, валидация, шифрование, сохранение.
/status — проверка тарифа и подключённого API.
"""
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.db.database import get_session
from bot.models.user import User
from bot.services.wb_api import validate_wb_token
from bot.utils.crypto import encrypt_token

router = Router(name="api_connect")

class ConnectStates(StatesGroup):
    waiting_key = State()

@router.message(Command("connect"))
async def cmd_connect(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🔐 <b>Подключение API Wildberries</b>\n\n"
        "Отправь свой API-ключ из личного кабинета WB.\n"
        "Ключ будет зашифрован и сохранён в безопасности.\n\n"
        "Чтобы отменить — напиши /cancel",
    )
    await state.set_state(ConnectStates.waiting_key)

@router.message(ConnectStates.waiting_key, F.text.startswith("/cancel"))
async def cancel_connect(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Подключение отменено.")

@router.message(ConnectStates.waiting_key)
async def process_key(message: Message, state: FSMContext) -> None:
    key = message.text.strip()
    if len(key) < 20:
        await message.answer("Ключ слишком короткий. Проверь и отправь снова:")
        return
    
    # Валидация через API WB
    await message.answer("⏳ Проверяю ключ...")
    is_valid, error = await validate_wb_token(key)
    
    if not is_valid:
        await message.answer(f"❌ Ошибка: {error}\n\nПроверь ключ и напиши /connect ещё раз.")
        await state.clear()
        return
    
    # Шифруем и сохраняем
    encrypted = encrypt_token(key)
    user_id = message.from_user.id
    
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=message.from_user.username)
            session.add(user)
        user.wb_api_key_encrypted = encrypted
        user.plan = "pro"  # Автоматически включаем Pro
        await session.commit()
    
    await state.clear()
    await message.answer(
        "✅ <b>API WB подключён!</b>\n\n"
        "Тариф Pro активирован.\n"
        "Теперь доступны:\n"
        "• Ежедневный дайджест прибыли\n"
        "• Алерты при падении маржи\n"
        "• Автозагрузка данных по всем SKU\n\n"
        "Напиши /status чтобы проверить статус."
    )

@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    user_id = message.from_user.id
    async with get_session() as session:
        user = await session.get(User, user_id)
    
    if not user:
        await message.answer("Ты ещё не зарегистрирован. Напиши /start")
        return
    
    plan = "Pro ✅" if user.plan == "pro" else "Free"
    wb = "Подключён ✅" if user.wb_api_key_encrypted else "Не подключён"
    digest = "Вкл ✅" if user.digest_enabled else "Выкл"
    alerts = "Вкл ✅" if user.alerts_enabled else "Выкл"
    
    await message.answer(
        f"📈 <b>Твой статус</b>\n\n"
        f"Тариф: {plan}\n"
        f"API WB: {wb}\n"
        f"Дайджест: {digest}\n"
        f"Алерты: {alerts}\n\n"
        f"Чтобы подключить Pro — напиши /connect"
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Текущая операция отменена.")