from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio

api = ''

bot = Bot(token=api)
dp = Dispatcher()

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
