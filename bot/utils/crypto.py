"""
ProfitRadar MP — Шифрование API-ключей (Fernet).
"""
from cryptography.fernet import Fernet
from bot.config import settings

def get_fernet() -> Fernet:
    """Получить экземпляр Fernet из ключа в .env."""
    if not settings.encryption_key:
        raise ValueError("ENCRYPTION_KEY не задан в .env")
    return Fernet(settings.encryption_key.encode())

def encrypt_token(token: str) -> str:
    """Зашифровать токен."""
    return get_fernet().encrypt(token.encode()).decode()

def decrypt_token(encrypted: str) -> str:
    """Расшифровать токен."""
    return get_fernet().decrypt(encrypted.encode()).decode()