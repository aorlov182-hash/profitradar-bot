"""
Админ-команды для просмотра статистики.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.db.database import engine
from bot.config import settings

router = Router(name="admin")


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    """Показывает статистику бота (только для админа)."""
    if message.from_user.id != settings.admin_user_id:
        await message.answer("Эта команда доступна только администратору.")
        return
    
    with engine.connect() as conn:
        # Общее количество уникальных пользователей
        total_users = conn.execute(text("SELECT COUNT(DISTINCT user_id) FROM stats")).scalar()
        
        # Активные за сегодня
        active_today = conn.execute(text("""
            SELECT COUNT(DISTINCT user_id) FROM stats 
            WHERE created_at >= date('now', 'start of day')
        """)).scalar()
        
        # Активные за неделю
        active_week = conn.execute(text("""
            SELECT COUNT(DISTINCT user_id) FROM stats 
            WHERE created_at >= date('now', '-7 days')
        """)).scalar()
        
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
        """)).scalar()
    
    # Формируем сообщение
    stats_text = "📊 <b>Статистика бота</b>\n\n"
    stats_text += f"👥 Всего пользователей: <b>{total_users}</b>\n"
    stats_text += f"📅 Активных сегодня: <b>{active_today}</b>\n"
    stats_text += f"📆 Активных за неделю: <b>{active_week}</b>\n\n"
    stats_text += f"🔔 В списке ожидания Pro: <b>{waitlist_count}</b>\n\n"
    stats_text += "<b>Топ команд:</b>\n"
    
    for action, count in top_commands:
        command = action.replace("command:", "")
        stats_text += f"• {command}: {count} раз\n"
    
    await message.answer(stats_text)