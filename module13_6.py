from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import asyncio

api = ''

bot = Bot(token=api)
dp = Dispatcher()

button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')

kb = ReplyKeyboardBuilder()
kb.add(button1).add(button2)

btn_inline1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
btn_inline2 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kb_inline = InlineKeyboardBuilder()
kb_inline.add(btn_inline2).add(btn_inline1)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(F.text, Command('start'))
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.',
                         reply_markup=kb.as_markup(resize_keyboard=True))


@dp.callback_query(F.data == 'info')
async def starter(callback: types.CallbackQuery):
    await callback.message.answer('Информация о боте')
    await callback.answer()


@dp.message(F.text == 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline.as_markup())


@dp.callback_query(F.data == 'formulas')
async def get_formulas(callback):
    await callback.message.answer('Для мужчин: (10 х вес в кг) + (6,25 х рост в см) – (5 х возраст в г) + 5')
    await callback.answer()


@dp.callback_query(F.data == 'calories')
async def set_age(callback, state: FSMContext):
    await callback.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)
    await callback.answer()


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
