# ProfitRadar MP — База данных

## Назначение

База данных ProfitRadar MP предназначена для хранения информации о пользователях, расчетах прибыли, подписках, платежах и интеграциях с маркетплейсами.

Основная база данных проекта:

PostgreSQL 15


---

# Общая структура

Основные сущности:

- users
- calculations
- subscriptions
- payments
- api_keys
- devices


Связи:


users

  |

  ├── calculations

  |

  ├── subscriptions

  |

  ├── payments

  |

  ├── api_keys

  |

  └── devices


---

# Таблица users

## Назначение

Хранит пользователей системы.


Поля:


id

Тип:

UUID

Описание:

Уникальный идентификатор пользователя.


telegram_id

Тип:

BIGINT

Описание:

ID пользователя Telegram.


username

Тип:

VARCHAR

Описание:

Имя пользователя Telegram.


email

Тип:

VARCHAR

Описание:

Email пользователя.


password_hash

Тип:

VARCHAR

Описание:

Хеш пароля (для веб-регистрации).


is_active

Тип:

BOOLEAN

Описание:

Активен ли пользователь.


created_at

Тип:

TIMESTAMP

Описание:

Дата создания аккаунта.


updated_at

Тип:

TIMESTAMP

Описание:

Дата последнего изменения.


---

# Таблица calculations

## Назначение

История расчётов прибыли.


Поля:


id

Тип:

UUID


user_id

Тип:

UUID

Связь:

users.id


product_name

Тип:

VARCHAR

Название товара.


purchase_price

Тип:

DECIMAL

Цена закупки.


selling_price

Тип:

DECIMAL

Цена продажи.


commission

Тип:

DECIMAL

Комиссия маркетплейса.


logistics

Тип:

DECIMAL

Логистика.


advertising

Тип:

DECIMAL

Реклама.


profit

Тип:

DECIMAL

Итоговая прибыль.


margin

Тип:

DECIMAL

Маржинальность.


created_at

Тип:

TIMESTAMP


---

# Таблица subscriptions

## Назначение

Хранение подписок пользователей.


Поля:


id

Тип:

UUID


user_id

Тип:

UUID


plan

Тип:

VARCHAR


Возможные значения:

FREE

PRO


status

Тип:

VARCHAR


Возможные значения:

active

expired

cancelled


start_date

Тип:

DATE


end_date

Тип:

DATE


created_at

Тип:

TIMESTAMP


---

# Таблица payments

## Назначение

История платежей.


Поля:


id

Тип:

UUID


user_id

Тип:

UUID


amount

Тип:

DECIMAL


currency

Тип:

VARCHAR


provider

Тип:

VARCHAR


Примеры:

ЮKassa

Stripe

Telegram Payments


status

Тип:

VARCHAR


created_at

Тип:

TIMESTAMP


---

# Таблица api_keys

## Назначение

Хранение ключей доступа к маркетплейсам.


Поля:


id

Тип:

UUID


user_id

Тип:

UUID


marketplace

Тип:

VARCHAR


Значения:

Wildberries

Ozon


encrypted_key

Тип:

TEXT


Описание:

Зашифрованный API ключ.


created_at

Тип:

TIMESTAMP


---

# Таблица devices

## Назначение

Подключенные устройства пользователя.


Поля:


id

Тип:

UUID


user_id

Тип:

UUID


device_type

Тип:

VARCHAR


Примеры:

Android

Web


device_token

Тип:

TEXT


Используется для:

Push-уведомлений.


created_at

Тип:

TIMESTAMP


---

# Индексы

Для ускорения работы:


users.telegram_id

INDEX


calculations.user_id

INDEX


subscriptions.user_id

INDEX


payments.user_id

INDEX


api_keys.user_id

INDEX


---

# Безопасность


Пароли:

- никогда не хранятся в открытом виде;
- используется хеширование.


API ключи маркетплейсов:

- хранятся только в зашифрованном виде;
- доступ имеет только пользователь.


Персональные данные:

- минимально необходимые;
- защищенное хранение.


---

# Миграции


Для управления изменениями структуры используется:


Alembic


Пример:


Создание новой таблицы

↓

Alembic migration

↓

Применение к PostgreSQL


---

# Будущие расширения


В дальнейшем могут быть добавлены:


## products

Каталог товаров пользователя.


## sales

Продажи с маркетплейсов.


## expenses

Дополнительные расходы.


## reports

Сохраненные отчеты.


## ai_recommendations

Ответы AI-аналитика.


---

# Целевая структура базы


PostgreSQL

|

├── users

├── products

├── calculations

├── sales

├── expenses

├── subscriptions

├── payments

├── api_keys

├── devices

└── ai_recommendations


---

# Текущее состояние


Сейчас:

MVP использует простое хранение данных.


Следующий этап:

Переход на PostgreSQL + SQLAlchemy + Alembic.


Цель:

Получить надежную коммерческую базу данных для SaaS-платформы ProfitRadar MP.