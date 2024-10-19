from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio

api = '7780851910:AAFlpxho6e15lfa52eedHI8YiENQlLrQKQQ'

bot = Bot(token=api)
dp = Dispatcher()

# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")
#     print('Привет! Я бот помогающий твоему здоровью.')


@dp.message(Command('start'))
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')

@dp.message()
async def all_messages(message):
    print('Введите команду /start, чтобы начать общение.')
    
async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())