import asyncio
from aiogram import Bot, Dispatcher, F
import requests
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from datetime import datetime, timedelta

from config import TOKEN
from config import NASA_API

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API}&date={date_str}"
    response = requests.get(url)
    return response.json()


@dp.message(Command("img"))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']
    description = None

    await message.answer_photo(photo=photo_url, caption=f'{title}\n \n{description}')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
