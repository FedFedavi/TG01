import asyncio
from aiogram import Bot, Dispatcher, F
import requests
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from datetime import datetime, timedelta

from config import TOKEN
from config import NEWS_API

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_wsj():
    url = f"https://newsapi.org/v2/everything?domains=wsj.com&apiKey={NEWS_API}"
    response = requests.get(url)
    return response.json()


def get_gen():
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey={NEWS_API}"
    response = requests.get(url)
    return response.json()


def get_search(search):
    url = f"https://newsapi.org/v2/everything?q={search}&searchIn=title&sortBy=popularity&apiKey={NEWS_API}"
    response = requests.get(url)
    return response.json()


@dp.message(Command("wsj"))
async def list_wsj(message: Message):
    news = get_wsj()
    if news['status'] == 'ok':
        articles = news['articles']
        for article in articles:
            title = article['title']
            source_name = article['source']['name']
            url = article['url']
            await message.answer(f"Источник: {source_name}\nЗаголовок: {title}\nСсылка: {url}")
    else:
        await message.answer("Не удалось получить новости WSJ.")


@dp.message(Command("general"))
async def list_news(message: Message):
    news = get_gen()
    if news['status'] == 'ok':
        articles = news['articles']
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            await message.answer(f"Заголовок: {title}\nОписание: {description}\nСсылка: {url}")
    else:
        await message.answer("Не удалось получить новости.")


@dp.message()
async def list_search(message: Message):
    search = message.text
    news = get_search(search)
    if news['status'] == 'ok':
        articles = news['articles'][:5]
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            await message.answer(f"Заголовок: {title}\nОписание: {description}\nСсылка: {url}")
    else:
        await message.answer("Не удалось получить новости по поиску слова.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
