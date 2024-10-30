from aiogram import Bot, Dispatcher, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
import asyncio

api = ''

bot = Bot(token=api)
dp = Dispatcher()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(F.text.contains('Calories'))
async def set_age(message, state: FSMContext):
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


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
    await state.update_data(weight=message.text)

    data=await state.get_data()
    result=10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5
    await message.answer(f'Ваша норма калорий: {result}')
    await state.clear()




async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
