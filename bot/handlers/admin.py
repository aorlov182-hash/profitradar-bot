"""
Админ-команды для просмотра статистики.
"""
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.db.database import engine
from bot.config import settings

logger = logging.getLogger(__name__)
router = Router(name="admin")


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    """Показывает статистику бота (только для админа)."""
    user_id = message.from_user.id
    logger.info(f"Получена команда /stats от пользователя ID: {user_id}")
    
    # Приводим admin_user_id к числу, чтобы сравнение с user_id (который всегда int) работало на 100%
    try:
        admin_id = int(settings.admin_user_id)
    except (ValueError, TypeError):
        logger.error("Ошибка: ADMIN_USER_ID в настройках не является числом!")
        await message.answer("Ошибка конфигурации админа. Проверьте .env")
        return

    if user_id != admin_id:
        logger.warning(f"Отказ в доступе: ваш ID ({user_id}) не совпадает с ADMIN_USER_ID ({admin_id})")
        await message.answer("Эта команда доступна только администратору.")
        return
    
    logger.info("Доступ разрешен. Запрашиваем статистику из БД...")
    
    try:
        with engine.connect() as conn:
            # Общее количество уникальных пользователей
            total_users = conn.execute(text("SELECT COUNT(DISTINCT user_id) FROM stats")).scalar() or 0
            
            # Активные за сегодня
            active_today = conn.execute(text("""
                SELECT COUNT(DISTINCT user_id) FROM stats 
                WHERE created_at >= date('now', 'start of day')
            """)).scalar() or 0
            
            # Активные за неделю
            active_week = conn.execute(text("""
                SELECT COUNT(DISTINCT user_id) FROM stats 
                WHERE created_at >= date('now', '-7 days')
            """)).scalar() or 0
            
            # Топ команд
            top_commands = conn.execute(text("""
                SELECT action, COUNT(*) as count 
                FROM stats 
                WHERE action LIKE 'command:%'
                GROUP BY action 
                ORDER BY count DESC 
                LIMIT 5
            """)).fetchall()
            
            # Количество нажатий "Напомнить о запуске"
            waitlist_count = conn.execute(text("""
                SELECT COUNT(*) FROM stats 
                WHERE action = 'callback:notify_pro'
            """)).scalar() or 0
        
        # Формируем сообщение
        stats_text = "📊 <b>Статистика бота</b>\n\n"
        stats_text += f"👥 Всего пользователей: <b>{total_users}</b>\n"
        stats_text += f"📅 Активных сегодня: <b>{active_today}</b>\n"
        stats_text += f"📆 Активных за неделю: <b>{active_week}</b>\n\n"
        stats_text += f"🔔 В списке ожидания Pro: <b>{waitlist_count}</b>\n\n"
        stats_text += "<b>Топ команд:</b>\n"
        
        if not top_commands:
            stats_text += "Пока нет данных о командах.\n"
        else:
            for action, count in top_commands:
                command = action.replace("command:", "")
                stats_text += f"• {command}: {count} раз\n"
        
        await message.answer(stats_text)
        logger.info("Статистика успешно отправлена пользователю.")
        
    except Exception as e:
        logger.error(f"Ошибка при получении статистики из БД: {e}")
        await message.answer("Произошла ошибка при чтении статистики. Проверьте логи.")