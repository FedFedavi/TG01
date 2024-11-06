import asyncio
from aiogram import Bot, Dispatcher, F
import requests
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random

from config import TOKEN
from config import THE_CAT_API

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_cat_breeds():
   url = "https://api.thecatapi.com/v1/breeds"
   headers = {'x-api-key': THE_CAT_API}
   response = requests.get(url, headers=headers)
   return response.json()


def get_cat_img(breed_id):
   url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
   headers = {'x-api-key': THE_CAT_API}
   response = requests.get(url, headers=headers)
   data = response.json()
   return data[0]['url']


def get_breed_info(breed_name):
   breeds = get_cat_breeds()
   for breed in breeds:
      if breed['name'].lower() == breed_name.lower():
         return breed
   return None


@dp.message(CommandStart())
async def start(message: Message):
   await message.answer('Привет, напиши мне название породы кошки, а я пришлю ее фото и информацию')


@dp.message(Command('breed'))
async def breed_list(message: Message):
   breed_list = get_cat_breeds()
   breed_names = [breed["name"] for breed in breed_list]
   await message.answer(f'Вот какие породы есть - {", ".join(breed_names)}')


@dp.message()
async def send_cat(message: Message):
   breed_name = message.text
   breed_info = get_breed_info(breed_name)
   if breed_info:
      cat_image_url = get_cat_img(breed_info['id'])
      info = (f'Порода - {breed_info["name"]}\n'
              f'Описание - {breed_info["description"]}\n'
              f'Продолжительность жизни - {breed_info["life_span"]} лет')
      await message.answer_photo(photo=cat_image_url, caption=info)
   else:
      await message.answer('Порода не найдена')




async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())