"""Регистрация меню команд бота (кнопка «/» в поле ввода Telegram)."""
from aiogram import Bot
from aiogram.types import BotCommand


BOT_COMMANDS = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="help", description="Список команд"),
    BotCommand(command="compare", description="Сравнить WB и Ozon"),
    BotCommand(command="calc", description="Калькулятор маржи"),
    BotCommand(command="app", description="Скачать Android-приложение"),
    BotCommand(command="pro", description="Тарифы и подключение Pro"),
    BotCommand(command="pay", description="Оплата Pro"),
    BotCommand(command="connect", description="Подключить API WB"),
    BotCommand(command="digest", description="Дайджест прибыли"),
    BotCommand(command="alerts", description="Алерты по марже"),
    BotCommand(command="cancel", description="Отменить текущий ввод"),
]


async def set_bot_commands(bot: Bot) -> None:
    """Регистрирует меню команд в мессенджере."""
    await bot.set_my_commands(BOT_COMMANDS)
