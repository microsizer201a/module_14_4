from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

initiate_db()

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_res = KeyboardButton(text="Рассчитать")
button_info = KeyboardButton(text="Информация")
button_buy = KeyboardButton(text="Купить")
kb.row(button_res)
kb.row(button_info)
kb.add(button_buy)

kb_s = InlineKeyboardMarkup()
button_s_res = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button_s_forms = InlineKeyboardButton(text="Формулы рассчета", callback_data="formulas")
kb_s.add(button_s_res)
kb_s.add(button_s_forms)

kb_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ]
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)

@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=kb_s)

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weigth(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f"Вашанорма калорий {res}")
    await state.finish()

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = get_all_products()
    for number in range(1,5):
        title = products[number-1][1]
        description = products[number-1][2]
        price = products[number-1][3]
        with open(f"files/{number}.jpg", "rb") as img:
            await message.answer_photo(img, f"Название: {title} | Описание: {description} | Цена: {price}")
    await message.answer("Выберите продукт для покупки", reply_markup=kb_buy)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт")
    await call.answer()

@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
