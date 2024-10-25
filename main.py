import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "Что такое ИИ?" )
async def aitext(message: Message):
    await message.answer('ИИ — это технология, позволяющая машинам выполнять задачи, требующие человеческого интеллекта.')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Ого какая фотка!", "Непонял, это где", "Давай еще", "))"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ["https://avatars.mds.yandex.net/i?id=d52244e4a21e7079c58e2870aaa2b58e14cb3bb9-12719281-images-thumbs&n=13",
            "https://avatars.mds.yandex.net/i?id=88597203364ee92eaff5bf5aaf820ff5f0f8ec94-5656601-images-thumbs&n=13",
            "https://avatars.mds.yandex.net/i?id=12c77f498e23b6d21f9ec5e4c74098b870062f69-12788981-images-thumbs&n=13",
            "https://avatars.mds.yandex.net/i?id=fa9b2f4de3aefd90e77b4c341fdc6433af48c24a-5216463-images-thumbs&n=13"]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='это мегакартинка')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(CommandStart)
async def start(message: Message):
    await message.answer('Приветики! Я бот')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

