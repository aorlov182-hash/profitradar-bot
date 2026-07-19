"""
ProfitRadar MP — Margin Calculator
Расчёт чистой маржи по товару для WB и Ozon.
Тарифы актуальны на июнь 2026 (ИРП WB 23.03.2026, Ozon 06.04.2026).
"""
from dataclasses import dataclass
from enum import Enum


class Marketplace(str, Enum):
    WB = "wb"
    OZON = "ozon"


@dataclass
class ProductInput:
    """Входные данные от пользователя."""
    marketplace: Marketplace
    category: str          # Категория товара
    sell_price: float      # Цена продажи, ₽
    cost_price: float      # Себестоимость, ₽
    weight_kg: float       # Вес, кг
    length_cm: float = 0   # Длина, см
    width_cm: float = 0    # Ширина, см
    height_cm: float = 0   # Высота, см
    tax_rate: float = 0.06 # Ставка налога (по умолчанию УСН 6%)


@dataclass
class MarginResult:
    """Результат расчёта."""
    sell_price: float
    cost_price: float
    commission: float
    logistics: float
    storage: float
    returns_cost: float
    tax: float
    net_profit: float
    margin_percent: float
    breakdown: dict


# ============================================================
# ТАРИФЫ (захардкожены для MVP, потом тянуть из API)
# ============================================================

# Комиссии WB по категориям (%, ИРП от 23.03.2026)
WB_COMMISSIONS = {
    "одежда": 0.15,
    "обувь": 0.15,
    "электроника": 0.12,
    "бытовая техника": 0.12,
    "красота": 0.14,
    "здоровье": 0.14,
    "дом и сад": 0.13,
    "детские товары": 0.13,
    "продукты": 0.10,
    "аксессуары": 0.15,
    "спорт": 0.14,
    "автотовары": 0.12,
    "default": 0.15,
}

# Комиссии Ozon по категориям (%, от 06.04.2026)
OZON_COMMISSIONS = {
    "одежда": 0.14,
    "обувь": 0.14,
    "электроника": 0.10,
    "бытовая техника": 0.10,
    "красота": 0.12,
    "здоровье": 0.12,
    "дом и сад": 0.12,
    "детские товары": 0.12,
    "продукты": 0.08,
    "аксессуары": 0.14,
    "спорт": 0.13,
    "автотовары": 0.10,
    "default": 0.13,
}

# Логистика (WB: зависит от объёмного веса, базовая ставка)
WB_LOGISTICS_BASE = 50.0        # Базовая доставка до покупателя, ₽
WB_LOGISTICS_PER_LITER = 8.0    # За каждый литр сверх 1л, ₽

# Логистика Ozon (FBO, базовая)
OZON_LOGISTICS_BASE = 75.0      # Базовая доставка, ₽
OZON_LOGISTICS_PER_KG = 15.0    # За каждый кг сверх 1 кг, ₽

# Хранение (в сутки за 1 литр объёма)
WB_STORAGE_PER_DAY_LITER = 0.8   # ₽/сутки/литр
OZON_STORAGE_PER_DAY_LITER = 0.9 # ₽/сутки/литр
AVG_STORAGE_DAYS = 30            # Средний срок хранения для оценки

# Средний % возвратов по категориям
RETURN_RATES = {
    "одежда": 0.25,
    "обувь": 0.30,
    "электроника": 0.05,
    "бытовая техника": 0.07,
    "красота": 0.08,
    "здоровье": 0.05,
    "дом и сад": 0.10,
    "детские товары": 0.12,
    "продукты": 0.02,
    "default": 0.10,
}

# Стоимость обработки возврата
WB_RETURN_COST = 50.0    # ₽ за возврат
OZON_RETURN_COST = 75.0  # ₽ за возврат


# ============================================================
# ФУНКЦИИ РАСЧЁТА
# ============================================================

def get_volume_liters(length_cm: float, width_cm: float, height_cm: float) -> float:
    """Объём товара в литрах."""
    if all([length_cm, width_cm, height_cm]):
        return (length_cm * width_cm * height_cm) / 1000
    return 1.0  # По умолчанию 1 литр


def get_commission_rate(marketplace: Marketplace, category: str) -> float:
    """Получить ставку комиссии по МП и категории."""
    category_lower = category.lower().strip()
    if marketplace == Marketplace.WB:
        return WB_COMMISSIONS.get(category_lower, WB_COMMISSIONS["default"])
    else:
        return OZON_COMMISSIONS.get(category_lower, OZON_COMMISSIONS["default"])


def get_return_rate(category: str) -> float:
    """Средний процент возвратов по категории."""
    return RETURN_RATES.get(category.lower().strip(), RETURN_RATES["default"])


def calc_logistics(product: ProductInput) -> float:
    """Рассчитать стоимость логистики."""
    volume = get_volume_liters(product.length_cm, product.width_cm, product.height_cm)
    if product.marketplace == Marketplace.WB:
        extra_liters = max(0, volume - 1.0)
        return WB_LOGISTICS_BASE + (extra_liters * WB_LOGISTICS_PER_LITER)
    else:
        extra_kg = max(0, product.weight_kg - 1.0)
        return OZON_LOGISTICS_BASE + (extra_kg * OZON_LOGISTICS_PER_KG)


def calc_storage(product: ProductInput, days: int = AVG_STORAGE_DAYS) -> float:
    """Рассчитать стоимость хранения за период."""
    volume = get_volume_liters(product.length_cm, product.width_cm, product.height_cm)
    if product.marketplace == Marketplace.WB:
        return volume * WB_STORAGE_PER_DAY_LITER * days
    else:
        return volume * OZON_STORAGE_PER_DAY_LITER * days


def calc_returns_cost(product: ProductInput) -> float:
    """Рассчитать стоимость возвратов (средняя на единицу)."""
    return_rate = get_return_rate(product.category)
    cost_per_return = (
        WB_RETURN_COST if product.marketplace == Marketplace.WB
        else OZON_RETURN_COST
    )
    return return_rate * cost_per_return


def calculate_margin(product: ProductInput) -> MarginResult:
    """
    Главная функция: расчёт чистой маржи.
    Формула:
    Чистая прибыль = Цена продажи
                     - Себестоимость
                     - Комиссия МП
                     - Логистика
                     - Хранение (за 1 ед. при среднем сроке)
                     - Возвраты (средние на 1 продажу)
                     - Налог
    """
    # Комиссия маркетплейса
    commission_rate = get_commission_rate(product.marketplace, product.category)
    commission = product.sell_price * commission_rate

    # Логистика
    logistics = calc_logistics(product)

    # Хранение (приведено к 1 единице товара, ~30 дней)
    storage = calc_storage(product)

    # Возвраты
    returns_cost = calc_returns_cost(product)

    # Налог (от выручки)
    tax = product.sell_price * product.tax_rate

    # Чистая прибыль
    net_profit = (
        product.sell_price
        - product.cost_price
        - commission
        - logistics
        - storage
        - returns_cost
        - tax
    )

    # Маржинальность
    margin_percent = (net_profit / product.sell_price * 100) if product.sell_price > 0 else 0

    return MarginResult(
        sell_price=product.sell_price,
        cost_price=product.cost_price,
        commission=round(commission, 2),
        logistics=round(logistics, 2),
        storage=round(storage, 2),
        returns_cost=round(returns_cost, 2),
        tax=round(tax, 2),
        net_profit=round(net_profit, 2),
        margin_percent=round(margin_percent, 1),
        breakdown={
            "commission_rate": f"{commission_rate*100:.0f}%",
            "return_rate": f"{get_return_rate(product.category)*100:.0f}%",
            "storage_days": AVG_STORAGE_DAYS,
            "tax_rate": f"{product.tax_rate*100:.0f}%",
        }
    )


def format_result(result: MarginResult, marketplace: Marketplace) -> str:
    """
    Форматировать результат для Telegram-сообщения.
    """
    mp_name = "Wildberries" if marketplace == Marketplace.WB else "Ozon"
    warning = ""
    if result.margin_percent < 15:
        warning = "\n⚠ Маржа тонкая! Любой скачок в возвратах или логистике может увести в минус."
    if result.margin_percent < 0:
        warning = "\n🚨 Товар убыточный! Ты теряешь деньги на каждой продаже."

    return (
        f"📊 Раскладка по {mp_name}:\n\n"
        f"💰 Цена продажи: {result.sell_price:.0f} ₽\n"
        f" Себестоимость: -{result.cost_price:.0f} ₽\n"
        f" Комиссия МП ({result.breakdown['commission_rate']}): -{result.commission:.0f} ₽\n"
        f"🚚 Логистика: -{result.logistics:.0f} ₽\n"
        f" Хранение (~{result.breakdown['storage_days']} дн.): -{result.storage:.0f} ₽\n"
        f"🔄 Возвраты (~{result.breakdown['return_rate']}): -{result.returns_cost:.0f} ₽\n"
        f"📝 Налог ({result.breakdown['tax_rate']}): -{result.tax:.0f} ₽\n\n"
        f"{'✅' if result.net_profit >= 0 else '❌'} Чистая прибыль: {result.net_profit:.0f} ₽\n"
        f"📈 Маржинальность: {result.margin_percent:.1f}%"
        f"{warning}"
    )


# ============================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ============================================================

if __name__ == "__main__":
    # Пример: футболка на WB
    product = ProductInput(
        marketplace=Marketplace.WB,
        category="одежда",
        sell_price=2500,
        cost_price=600,
        weight_kg=0.3,
        length_cm=30,
        width_cm=20,
        height_cm=3,
        tax_rate=0.06,
    )
    result = calculate_margin(product)
    print(format_result(result, product.marketplace))
    print()

    # Пример: наушники на Ozon
    product2 = ProductInput(
        marketplace=Marketplace.OZON,
        category="электроника",
        sell_price=4500,
        cost_price=1800,
        weight_kg=0.25,
        length_cm=15,
        width_cm=10,
        height_cm=5,
        tax_rate=0.06,
    )
    result2 = calculate_margin(product2)
    print(format_result(result2, product2.marketplace))