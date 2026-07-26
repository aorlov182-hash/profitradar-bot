from bot.db.database import get_session
from bot.models.user import User


async def check_pro(user_id: int) -> bool:
    async with get_session() as session:
        user = await session.get(User, user_id)

        if not user:
            return False

        return user.tariff == "PRO"