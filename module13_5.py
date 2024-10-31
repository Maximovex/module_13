from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

api = ''

bot = Bot(token=api)
dp = Dispatcher()
#buttons = [[KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]]
#kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
button1=KeyboardButton(text='Рассчитать')
button2=KeyboardButton(text='Информация')

kb=ReplyKeyboardBuilder()
kb.add(button1).add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(F.text.contains('Рассчитать'))
async def set_age(message, state: FSMContext):
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(F.text, Command('start'))
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb.as_markup(resize_keyboard=True))


@dp.message(F.text.contains('Информация'))
async def inform(message):
    await message.answer('Информация о боте')


@dp.message(UserState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см):')
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес(кг):')
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def calculate(message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {result}')
    await state.clear()


@dp.message()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
