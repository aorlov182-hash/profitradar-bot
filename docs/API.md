# ProfitRadar MP — Backend API

## Назначение

Backend API является центральной частью платформы ProfitRadar MP.

Все клиенты системы взаимодействуют исключительно через Backend API.

Клиенты:

- Telegram Bot
- Android App
- Website
- будущие сервисы

Backend отвечает за:

- авторизацию;
- хранение данных;
- подписки;
- расчеты;
- API Wildberries;
- API Ozon;
- AI-анализ;
- уведомления.

---

# Технологии

Backend разрабатывается на:

- Python 3.13+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Pydantic v2
- Uvicorn

---

# Формат обмена

Все запросы используют:

JSON

Ответы сервера также возвращаются в формате JSON.

---

# Авторизация

Все защищённые запросы используют JWT.

Пример заголовка:

Authorization: Bearer <access_token>

---

# Основные разделы API

## AUTH

Авторизация пользователя.

Планируемые методы:

POST /auth/login

POST /auth/refresh

POST /auth/logout

GET /auth/me

---

## USERS

Работа с пользователем.

GET /users/me

PATCH /users/me

GET /users/devices

DELETE /users/device/{id}

---

## SUBSCRIPTIONS

Работа с подписками.

GET /subscriptions/status

POST /subscriptions/create

POST /subscriptions/cancel

GET /subscriptions/history

---

## PAYMENTS

Оплата подписки.

POST /payments/create

POST /payments/webhook

GET /payments/history

---

## CALCULATIONS

История расчётов.

GET /calculations

POST /calculations

GET /calculations/{id}

DELETE /calculations/{id}

---

## API KEYS

Управление API маркетплейсов.

GET /api-keys

POST /api-keys

PATCH /api-keys/{id}

DELETE /api-keys/{id}

---

## MARKETPLACES

Работа с маркетплейсами.

POST /wb/import

POST /ozon/import

GET /marketplaces/status

---

## AI

AI-аналитика.

POST /ai/analyze

POST /ai/recommend

POST /ai/forecast

---

## NOTIFICATIONS

Уведомления.

GET /notifications

PATCH /notifications/read

DELETE /notifications/{id}

---

# Ответы сервера

Успешный ответ:

```json
{
  "success": true,
  "data": {}
}
```

Ошибка:

```json
{
  "success": false,
  "error": "Описание ошибки"
}
```

---

# Версионирование

Все API будут иметь версию.

Пример:

/api/v1/

В будущем:

/api/v2/

Это позволит обновлять систему без нарушения совместимости.

---

# Ограничение запросов

Backend использует Rate Limit.

Например:

100 запросов в минуту.

При превышении лимита возвращается ошибка:

HTTP 429 Too Many Requests

---

# Документация

FastAPI автоматически предоставляет:

Swagger UI

/docs

и

ReDoc

/redoc

---

# Безопасность

Backend использует:

- HTTPS;
- JWT;
- проверку прав доступа;
- валидацию данных;
- шифрование чувствительной информации;
- логирование ошибок.

---

# Масштабирование

Архитектура API проектируется таким образом, чтобы в будущем можно было добавить:

- iOS-приложение;
- Desktop-клиент;
- интеграции с CRM;
- партнерский API;
- публичный API.

Без изменения существующей структуры.

---

# Итог

Backend API является единой точкой взаимодействия всех компонентов ProfitRadar MP.

Любая новая функция сначала реализуется в Backend API и только после этого становится доступной в Telegram-боте, Android-приложении и на сайте.