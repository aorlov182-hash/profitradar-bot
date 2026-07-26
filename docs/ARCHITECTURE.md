# ProfitRadar MP — Архитектура системы

> Версия документа: 1.0
> Статус: Draft
> Последнее обновление: 26.07.2026

---

# Общая архитектура

ProfitRadar MP строится как единая платформа.

Все клиенты используют один Backend API и одну общую базу данных.

```
                    +----------------------+
                    |      Android App     |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |      Backend API     |
                    |       FastAPI        |
                    +----------+-----------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          |                    |                    |
+---------v---------+  +-------v--------+  +--------v---------+
| PostgreSQL        |  | Telegram Bot   |  | Website          |
| Render Database   |  | aiogram 3.x    |  | Landing / Web    |
+-------------------+  +----------------+  +------------------+
```

---

# Компоненты системы

## Telegram Bot

Назначение:

- быстрый расчёт прибыли;
- уведомления;
- работа с подпиской;
- авторизация пользователя;
- запуск Android-приложения.

Технологии:

- Python
- aiogram 3.x
- Webhook
- Render

---

## Android App

Назначение:

- мобильная работа;
- история расчётов;
- просмотр аналитики;
- работа с PRO;
- AI-рекомендации.

Технологии:

- Flutter
- Material Design
- REST API

---

## Website

Назначение:

- описание продукта;
- установка приложения;
- оформление подписки;
- документация;
- новости проекта.

---

## Backend API

Главный компонент системы.

Отвечает за:

- пользователей;
- авторизацию;
- JWT;
- подписки;
- расчёты;
- хранение данных;
- AI;
- API Wildberries;
- API Ozon.

Технологии:

- Python
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic
- Uvicorn

---

## Database

Используется единая база PostgreSQL.

Планируемые таблицы:

- users
- subscriptions
- api_keys
- calculations
- payments
- devices

---

# Потоки данных

## Авторизация

```
Android

↓

Открывает Telegram Bot

↓

Пользователь подтверждает вход

↓

Backend API

↓

JWT Access Token

↓

Android получает доступ
```

---

## Расчёт прибыли

```
Android

↓

Backend API

↓

Расчёт

↓

PostgreSQL

↓

Ответ пользователю
```

---

## Работа Telegram

```
Пользователь

↓

Telegram

↓

Webhook

↓

Bot

↓

Backend API

↓

Ответ пользователю
```

---

# Инфраструктура

## Backend

Render Web Service

---

## Database

Render PostgreSQL

---

## Telegram

Webhook

---

## Android

APK

Google Play (после публикации)

---

## Domain

Cloudflare

---

# Авторизация

Используется единая система авторизации.

Основные технологии:

- Telegram Login
- JWT Access Token
- JWT Refresh Token

Планируется отказаться от постоянных API-ключей пользователя для входа.

---

# Безопасность

Используются:

- HTTPS
- JWT
- Шифрование API-ключей
- Проверка подписи Telegram
- Валидация запросов
- Ограничение частоты запросов (Rate Limit)

---

# Масштабирование

Архитектура должна позволять без серьёзной переработки добавить:

- iOS;
- Web Dashboard;
- AI Assistant;
- несколько Telegram-ботов;
- новые маркетплейсы;
- международные версии.

---

# Основные технологии

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Alembic

## Telegram

- aiogram 3.x

## Android

- Flutter

## Database

- PostgreSQL

## Hosting

- Render

## CDN / DNS

- Cloudflare

---

# Принципы разработки

1. Один источник бизнес-логики — Backend API.
2. Все клиенты используют одинаковые API.
3. Документация обновляется раньше кода.
4. Любое изменение архитектуры фиксируется в документации.
5. Все новые функции должны быть совместимы с существующей архитектурой.

---

# Текущее состояние

## Выполнено

- Telegram Bot
- Render Deploy
- Android MVP
- Webhook
- Scheduler

## Планируется

- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Backend API
- JWT
- PRO-подписка
- AI-модуль
- Web Dashboard

---

# Следующий документ

После утверждения архитектуры начинается описание структуры базы данных в файле:

DATABASE.md