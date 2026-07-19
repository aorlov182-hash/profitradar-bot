from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    db_url: str = "sqlite+aiosqlite:///./data/bot.db"
    encryption_key: str = ""
    admin_user_id: int = 631488568

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()