from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.db.database import get_session
from bot.models.user import User

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    # Сохраняем юзера в БД
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=username)
            session.add(user)
        else:
            user.username = username
        await session.commit()

    # Создаем кнопку со ссылкой на сайт
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Перейти на наш сайт", url="https://aorlov182-hash.github.io/profitradar-site/")]
        ]
    )

    await message.answer(
        "Привет! Я ProfitRadar 📈\n\n"
        "Помогу быстро посчитать реальную маржу по твоим "
        "товарам на WB или Ozon. Без Excel, без регистрации.\n\n"
        "Просто скинь данные по товару и получишь "
        "раскладку по всем расходам. Начнём?",
        reply_markup=keyboard
    )


HELP_TEXT = (
    "<b>Команды ProfitRadar</b>\n\n"
    "⚖️ /compare — сравнить, где выгоднее: WB или Ozon (бесплатно)\n"
    "📉 /calc — калькулятор маржи (бесплатно)\n"
    "📱 /app — скачать Android-приложение (офлайн-калькулятор)\n"
    "🏁 /start — вернуться в начало\n"
    "📚 /help — эта справка\n\n"
    "💰 <b>Pro (990 ₽/мес):</b>\n"
    "💳 /pay — оплата и тарифы\n"
    "🔗 /connect — подключить API WB/Ozon\n"
    "📬 /digest — ежедневный дайджест прибыли\n"
    "🚨 /alerts — алерты при падении маржи\n\n"
    "❌ /cancel — отменить текущий ввод\n\n"
    "Бесплатный калькулятор — без лимитов и без регистрации.\n"
    "Pro — API WB/Ozon, дайджесты и алерты по марже."
)

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """Отмена любого текущего ввода (сброс FSM)."""
    if await state.get_state() is None:
        await message.answer("Сейчас нет активного ввода. Начни с /start или /help 🙂")
        return
    await state.clear()
    await message.answer("❌ Текущий ввод отменён. Напиши /help, чтобы увидеть команды.")
