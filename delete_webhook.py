from aiogram import Bot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def delete_webhook():
    token = os.getenv("BOT_TOKEN")
    bot = Bot(token=token)
    
    await bot.delete_webhook()
    print("✅ Вебхук удалён! Теперь можно запускать бота.")
    
    await bot.close()

if __name__ == "__main__":
    asyncio.run(delete_webhook())