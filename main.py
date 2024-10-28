import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from gtts import gTTS
import os

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video/video.mp4")
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile("audio/bird.mp3")
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка №1. \n Приседания со штангой: 3 подхода по 10 повторений \nЖим лежа: 3 подхода по 8 повторений \nТяга блока к груди: 3 подхода по 12 повторений",
        "Тренировка №2. \nВыпады с гантелями: 3 подхода по 10 повторений на каждую ногу \nТяга штанги в наклоне: 3 подхода по 10 повторений \nЖим гантелей сидя: 3 подхода по 12 повторений",
        "Тренировка №3. \nПодъем на носки стоя: 3 подхода по 15 повторений \nПодтягивания на перекладине: 3 подхода по 6-8 повторений \nСкручивания на пресс: 3 подхода по 15 повторений"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("audio/training.mp3")
    audio = FSInputFile("audio/training.mp3")
    await bot.send_audio(message.chat.id, audio)
    os.remove("audio/training.mp3")



@dp.message(F.text == "Что такое ИИ?" )
async def aitext(message: Message):
    await message.answer('ИИ — это технология, позволяющая машинам выполнять задачи, требующие человеческого интеллекта.')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Ого какая фотка!", "Непонял, это где", "Давай еще", "))"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(Command('photo', prefix='&'))
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

@dp.message(CommandStart())
async def start2(message: Message):
    name = message.from_user.first_name
    await message.answer(f'Привет {name}, как дела?')


@dp.message()
async def start(message: Message):
    if message.text.lower() == 'тест':
        await message.answer('Тестируем')
    else:
        await start1(message)

@dp.message()
async def start1(message: Message):
    await message.send_copy(chat_id=message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

