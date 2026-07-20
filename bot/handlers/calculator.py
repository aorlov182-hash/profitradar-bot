"""
ProfitRadar MP — FSM-калькулятор маржи.
Пошаговый ввод данных: МП → категория → цена → себестоимость → вес.
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
    format_result,
)

router = Router(name="calculator")

class CalcStates(StatesGroup):
    marketplace = State()
    category = State()
    sell_price = State()
    cost_price = State()
    weight = State()

# Клавиатура выбора маркетплейса
MP_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Wildberries"), KeyboardButton(text="Ozon")],
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True,
)

CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
)

RECALC_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📊 Посчитать ещё")]],
    resize_keyboard=True,
)

@router.message(Command("calc"))
async def cmd_calc(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "📊 <b>Калькулятор маржи</b>\n\n"
        "Выбери маркетплейс:",
        reply_markup=MP_KEYBOARD,
    )
    await state.set_state(CalcStates.marketplace)

@router.message(CalcStates.marketplace, F.text.in_(["Wildberries", "Ozon"]))
async def process_marketplace(message: Message, state: FSMContext) -> None:
    mp = "wb" if message.text == "Wildberries" else "ozon"
    await state.update_data(marketplace=mp)
    await message.answer(
        "Введи категорию товара (например: одежда, электроника, обувь):",
        reply_markup=CANCEL_KEYBOARD,
    )
    await state.set_state(CalcStates.category)

@router.message(CalcStates.marketplace, F.text == "❌ Отмена")
async def cancel_calc_mp(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Калькулятор отменён. Напиши /calc чтобы начать заново.")

@router.message(CalcStates.category, F.text == "❌ Отмена")
async def cancel_calc_category(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Калькулятор отменён.")

@router.message(CalcStates.category)
async def process_category(message: Message, state: FSMContext) -> None:
    await state.update_data(category=message.text.lower().strip())
    await message.answer(
        "Введи цену продажи (₽):",
        reply_markup=CANCEL_KEYBOARD,
    )
    await state.set_state(CalcStates.sell_price)

@router.message(CalcStates.sell_price, F.text == "❌ Отмена")
async def cancel_calc_sell(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Калькулятор отменён.")

@router.message(CalcStates.sell_price)
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
    await state.set_state(CalcStates.cost_price)

@router.message(CalcStates.cost_price, F.text == "❌ Отмена")
async def cancel_calc_cost(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Калькулятор отменён.")

@router.message(CalcStates.cost_price)
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
    await state.set_state(CalcStates.weight)

@router.message(CalcStates.weight, F.text == "❌ Отмена")
async def cancel_calc_weight(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Калькулятор отменён.")

@router.message(CalcStates.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    try:
        weight = float(message.text.replace(",", "."))
        if weight <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Неверный вес. Введи число больше 0:")
        return

    # Получаем данные из FSM state
    data = await state.get_data()
    
    product = ProductInput(
        marketplace=Marketplace(data["marketplace"]),
        category=data["category"],
        sell_price=data["sell_price"],
        cost_price=data["cost_price"],
        weight_kg=weight,
    )

    result = calculate_margin(product)
    text = format_result(result, product.marketplace)

    await state.clear()
    await message.answer(
        text,
        reply_markup=RECALC_KEYBOARD,
    )

@router.message(F.text == "📊 Посчитать ещё")
async def recalc(message: Message, state: FSMContext) -> None:
    await cmd_calc(message, state)