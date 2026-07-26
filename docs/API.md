# ProfitRadar MP — API документация


## Назначение

Backend API является центральным компонентом платформы ProfitRadar MP.

Через API взаимодействуют:

- Telegram Bot;
- Android приложение;
- Website;
- AI-модули;
- внешние сервисы.


Основная технология:

- Python
- FastAPI


Формат обмена данными:

JSON


Версия API:

v1


---

# Базовый URL


Production:

https://profitradar-api.onrender.com/api/v1


Development:

http://localhost:8000/api/v1


---

# Авторизация


Тип:

JWT Authentication


Используется:

- Access Token
- Refresh Token


Заголовок запроса:


Authorization: Bearer TOKEN


---

# Пользовательские методы


## Регистрация пользователя


POST

/users/register


Описание:

Создание нового пользователя.


Request:


{
 "email": "user@example.com",
 "password": "password"
}


Response:


{
 "id": "uuid",
 "email": "user@example.com"
}


---

## Получение профиля


GET

/users/me


Response:


{
 "id": "uuid",
 "telegram_id":123456,
 "subscription":"PRO"
}


---

# Telegram авторизация


## Авторизация через Telegram


POST

/auth/telegram


Назначение:

Связывает Telegram аккаунт с пользователем.


Request:


{
 "telegram_id":123456,
 "username":"seller"
}


Response:


{
 "access_token":"JWT",
 "refresh_token":"JWT"
}


---

# Расчеты прибыли


## Создать расчет


POST

/calculations


Описание:

Создание нового расчета прибыли товара.


Request:


{
 "product_name":"Товар",
 "purchase_price":500,
 "selling_price":1500,
 "commission":300,
 "logistics":150,
 "advertising":100
}


Response:


{
 "profit":450,
 "margin":30
}


---

## История расчетов


GET

/calculations


Описание:

Получение истории пользователя.


Response:


[
 {
  "product_name":"Товар",
  "profit":450
 }
]


---

# Подписки


## Получить текущую подписку


GET

/subscription


Response:


{
 "plan":"PRO",
 "status":"active"
}


---

## Изменить тариф


POST

/subscription/change


Request:


{
 "plan":"PRO"
}


---

# Платежи


## Создание платежа


POST

/payments/create


Request:


{
 "plan":"PRO"
}


Response:


{
 "payment_url":"https://..."
}


---

# Маркетплейсы


## Добавить API ключ


POST

/marketplaces/connect


Request:


{
 "marketplace":"wildberries",
 "api_key":"encrypted_key"
}


---

## Получить статус подключения


GET

/marketplaces/status


Response:


{
 "wildberries":"connected",
 "ozon":"not_connected"
}


---

# AI аналитика


## Получить AI рекомендацию


GET

/ai/recommendation


Response:


{
 "message":
 "Увеличьте цену товара на 5%"
}


---

# Уведомления


## Получение настроек уведомлений


GET

/notifications/settings


---

## Изменение настроек


POST

/notifications/settings


---

# Коды ответов


200

Успешный запрос.


201

Создан новый объект.


400

Ошибка данных.


401

Необходима авторизация.


403

Недостаточно прав.


404

Объект не найден.


500

Ошибка сервера.


---

# Безопасность


API использует:


- HTTPS;
- JWT;
- шифрование API ключей;
- ограничение запросов;
- проверку прав доступа.


---

# Будущие расширения


Планируется:


- WebSocket уведомления;
- GraphQL API;
- интеграция 1С;
- интеграция МойСклад;
- партнерский API.


---

# Текущее состояние


Сейчас:

Telegram Bot работает напрямую.


Следующий этап:

Создание полноценного Backend API.


Цель:

Единый сервер для всей экосистемы ProfitRadar MP.