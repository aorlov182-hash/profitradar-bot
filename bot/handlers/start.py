"""
ProfitRadar MP — /start и /help.
Сохраняет юзера в БД при первом запуске.
"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
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
            user.username = username  # обновляем username
        await session.commit()

    await message.answer(
        "Привет! Я ProfitRadar 📡\n\n"
        "Помогу быстро посчитать реальную маржу по твоим "
        "товарам на WB или Ozon. Без Excel, без регистрации.\n\n"
        "Просто скинь данные по товару и получишь "
        "раскладку по всем расходам. Начнём?\n\n"
        "📊 /calc — калькулятор маржи\n"
        "📦 /pro — тарифы\n"
        "❓ /help — все команды"
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        " <b>Команды ProfitRadar</b>\n\n"
        "📊 /calc — калькулятор маржи (бесплатно)\n"
        "📦 /pro — тарифы и подключение Pro\n"
        " /connect — подключить API WB\n"
        "📈 /status — проверить тариф и API\n"
        "📬 /digest — дайджест прибыли (Pro)\n"
        "🚨 /alerts — алерты по марже (Pro)\n"
        "❌ /cancel — отменить текущий ввод\n\n"
        "Бесплатный калькулятор — без лимитов.\n"
        "Pro (990 ₽/мес) — API WB/Ozon, дайджесты, алерты."
    )