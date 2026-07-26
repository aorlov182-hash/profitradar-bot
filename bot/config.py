from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str

    webhook_url: str = ""

    db_url: str = "sqlite+aiosqlite:///./data/bot.db"

    encryption_key: str = ""

    admin_user_id: int = 631488568


    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


settings = Settings()