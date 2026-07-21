"""
ProfitRadar MP — Сравнение маржи WB и Ozon.
/compare — пошаговый ввод данных и сравнение прибыли на двух площадках.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.services.margin_calc import (
    Marketplace,
    ProductInput,
    calculate_margin,
)

router = Router(name="compare")

class CompareStates(StatesGroup):
    category = State()
    sell_price = State()
    cost_price = State()
    weight = State()

CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
)

RECALC_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📊 Сравнить ещё раз")]],
    resize_keyboard=True,
)

@router.message(Command("compare"))
async def cmd_compare(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "⚖️ <b>Сравнение маржи: Wildberries vs Ozon</b>\n\n"
        "Введи категорию товара (например: одежда, электроника, обувь):",
        reply_markup=CANCEL_KEYBOARD,
    )
    await state.set_state(CompareStates.category)

@router.message(CompareStates.category, F.text == "❌ Отмена")
async def cancel_compare(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Сравнение отменено.")

@router.message(CompareStates.category)
async def process_category(message: Message, state: FSMContext) -> None:
    await state.update_data(category=message.text.lower().strip())
    await message.answer(
        "Введи цену продажи (₽):",
        reply_markup=CANCEL_KEYBOARD,
    )
    await state.set_state(CompareStates.sell_price)

@router.message(CompareStates.sell_price, F.text == "❌ Отмена")
async def cancel_sell(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Сравнение отменено.")

@router.message(CompareStates.sell_price)
async def process_sell_price(message: Message, state: FSMContext) -> None:
    try:
        price = float(message.text.replace(",", "."))
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Неверная цена. Введи число больше 0:")
        return
    await state.update_data(sell_price=price)
    await message.answer("Введи себестоимость (₽):")
    await state.set_state(CompareStates.cost_price)

@router.message(CompareStates.cost_price, F.text == "❌ Отмена")
async def cancel_cost(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Сравнение отменено.")

@router.message(CompareStates.cost_price)
async def process_cost_price(message: Message, state: FSMContext) -> None:
    try:
        cost = float(message.text.replace(",", "."))
        if cost < 0:
            raise ValueError
    except ValueError:
        await message.answer("Неверная себестоимость. Введи число >= 0:")
        return
    await state.update_data(cost_price=cost)
    await message.answer(
        "Введи вес товара в кг (например: 0.3):",
        reply_markup=CANCEL_KEYBOARD,
    )
    await state.set_state(CompareStates.weight)

@router.message(CompareStates.weight, F.text == "❌ Отмена")
async def cancel_weight(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Сравнение отменено.")

@router.message(CompareStates.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    try:
        weight = float(message.text.replace(",", "."))
        if weight <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Неверный вес. Введи число больше 0:")
        return

    data = await state.get_data()
    
    # Создаём два объекта продукта для разных маркетплейсов
    product_wb = ProductInput(
        marketplace=Marketplace.WB,
        category=data["category"],
        sell_price=data["sell_price"],
        cost_price=data["cost_price"],
        weight_kg=weight,
    )
    
    product_ozon = ProductInput(
        marketplace=Marketplace.OZON,
        category=data["category"],
        sell_price=data["sell_price"],
        cost_price=data["cost_price"],
        weight_kg=weight,
    )

    result_wb = calculate_margin(product_wb)
    result_ozon = calculate_margin(product_ozon)

    # Форматирование чисел
    def fmt(v):
        return f"{v:,.0f} ₽".replace(",", " ")
    def fmt_dec(v):
        return f"{v:,.2f} ₽".replace(",", " ")

    # Определяем победителя
    if result_wb.net_profit > result_ozon.net_profit:
        winner = "🟣 Wildberries"
        diff = result_wb.net_profit - result_ozon.net_profit
    elif result_ozon.net_profit > result_wb.net_profit:
        winner = "🔵 Ozon"
        diff = result_ozon.net_profit - result_wb.net_profit
    else:
        winner = "🤝 Одинаково выгодно"
        diff = 0

    text = (
        f"⚖️ <b>Сравнение для категории: {data['category'].capitalize()}</b>\n"
        f"Цена: {fmt(data['sell_price'])} | Себестоимость: {fmt(data['cost_price'])} | Вес: {weight} кг\n\n"
        
        f"🟣 <b>Wildberries</b>\n"
        f"• Комиссия: {fmt(result_wb.commission)}\n"
        f"• Логистика: {fmt(result_wb.logistics)}\n"
        f"• Возвраты: {fmt(result_wb.returns_cost)}\n"
        f"• Чистая прибыль: <b>{fmt_dec(result_wb.net_profit)}</b>\n"
        f"• Маржинальность: <b>{result_wb.margin_percent:.1f}%</b>\n\n"
        
        f"🔵 <b>Ozon</b>\n"
        f"• Комиссия: {fmt(result_ozon.commission)}\n"
        f"• Логистика: {fmt(result_ozon.logistics)}\n"
        f"• Возвраты: {fmt(result_ozon.returns_cost)}\n"
        f"• Чистая прибыль: <b>{fmt_dec(result_ozon.net_profit)}</b>\n"
        f"• Маржинальность: <b>{result_ozon.margin_percent:.1f}%</b>\n\n"
        
        f"🏆 <b>Вывод:</b> Выгоднее продавать на <b>{winner}</b>\n"
        f"Разница в прибыли: <b>+{fmt_dec(diff)}</b> с каждой продажи."
    )

    await state.clear()
    await message.answer(text, reply_markup=RECALC_KEYBOARD)

@router.message(F.text == "📊 Сравнить ещё раз")
async def recalc_compare(message: Message, state: FSMContext) -> None:
    await cmd_compare(message, state)