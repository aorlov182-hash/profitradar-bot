# ProfitRadar MP — База данных

## Назначение

В качестве основной базы данных используется PostgreSQL.

SQLite использовалась только на этапе MVP и локальной разработки.

После перехода на PostgreSQL все новые функции работают только с ней.

---

# Основные принципы

База данных должна обеспечивать:

- высокую скорость работы;
- безопасность хранения данных;
- масштабируемость;
- поддержку миллионов записей;
- простоту резервного копирования;
- удобство миграций через Alembic.

---

# ORM

Для работы с базой используется:

- SQLAlchemy 2.x
- Alembic

SQL-запросы вручную практически не используются.

Вся работа ведётся через ORM.

---

# Основные таблицы

## users

Хранение пользователей системы.

Основные поля:

- id
- telegram_id
- username
- first_name
- last_name
- language
- is_admin
- created_at
- updated_at

---

## subscriptions

Информация о подписках.

Основные поля:

- id
- user_id
- plan
- status
- started_at
- expires_at
- auto_renew

---

## payments

История оплат.

Основные поля:

- id
- user_id
- provider
- amount
- currency
- status
- transaction_id
- created_at

---

## api_keys

API Wildberries и Ozon.

Ключи всегда хранятся в зашифрованном виде.

Основные поля:

- id
- user_id
- marketplace
- encrypted_key
- created_at
- updated_at
- is_active

---

## calculations

История расчётов прибыли.

Основные поля:

- id
- user_id
- marketplace
- purchase_price
- selling_price
- commission
- logistics
- advertising
- taxes
- profit
- margin
- created_at

---

## devices

Устройства пользователя.

Используется для синхронизации между Android, Web и Telegram.

Основные поля:

- id
- user_id
- platform
- device_name
- last_seen
- created_at

---

# Связи

users

↓

subscriptions

↓

payments

↓

api_keys

↓

calculations

↓

devices

Каждый пользователь может иметь:

- несколько устройств;
- несколько оплат;
- множество расчётов;
- несколько API-ключей.

---

# Индексы

Для ускорения работы используются индексы:

users.telegram_id

subscriptions.user_id

payments.user_id

api_keys.user_id

calculations.user_id

devices.user_id

---

# Шифрование

Конфиденциальные данные никогда не хранятся открытым текстом.

Шифруются:

- API Wildberries;
- API Ozon;
- токены доступа;
- служебные секреты.

Используется библиотека cryptography (Fernet).

---

# Миграции

Изменение структуры базы производится исключительно через Alembic.

Ручное изменение структуры PostgreSQL запрещается.

Каждое изменение сопровождается отдельной миграцией.

---

# Резервное копирование

База данных должна регулярно резервироваться.

Минимальные требования:

- ежедневный Backup;
- хранение последних 30 копий;
- возможность полного восстановления.

---

# Будущее развитие

Планируется добавление новых таблиц:

- ai_reports
- notifications
- audit_logs
- support_tickets
- marketplace_statistics
- competitors
- recommendations
- forecasts

Это позволит расширять систему без изменения существующей архитектуры.