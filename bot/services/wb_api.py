"""
ProfitRadar MP — Wildberries API client.
Валидация токена и получение данных.
"""
import httpx
from typing import Tuple

WB_API_BASE = "https://marketplace-api.wildberries.ru"

async def validate_wb_token(token: str) -> Tuple[bool, str]:
    """
    Проверить валидность API-ключа WB.
    Возвращает (True, "") если ключ валиден, или (False, "ошибка") если нет.
    """
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Пробуем сделать простой запрос к API
            response = await client.get(
                f"{WB_API_BASE}/api/v1/settings",
                headers=headers,
            )
            
            if response.status_code == 200:
                return True, ""
            elif response.status_code == 401:
                return False, "Неверный API-ключ"
            elif response.status_code == 403:
                return False, "Доступ запрещён. Проверь права доступа ключа."
            else:
                return False, f"Ошибка API: {response.status_code}"
                
    except httpx.TimeoutException:
        return False, "Превышено время ожидания ответа от WB"
    except httpx.NetworkError:
        return False, "Ошибка сети. Проверь интернет-соединение"
    except Exception as e:
        return False, f"Неизвестная ошибка: {str(e)}"


async def get_wb_income(token: str, date_from: str, date_to: str) -> dict:
    """
    Получить данные о доходах из WB API.
    (Заглушка для MVP, в реальной версии будет запрос к API)
    """
    # TODO: Реальный запрос к API WB для получения отчёта о продажах
    return {
        "income": 0,
        "orders": 0,
    }