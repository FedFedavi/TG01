import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery


from config import TOKEN
from googletrans import Translator
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('_____', reply_markup=kb.main)


@dp.callback_query(F.data == 'view')
async def view(callback: CallbackQuery):
    await callback.message.edit_text('_____', reply_markup=kb.inline_keyboard_op)


@dp.callback_query(F.data == 'Опция 1')
async def op1(callback: CallbackQuery):
    await callback.message.answer('Это текст при нажатии инлайн кнопки Опция 1')


@dp.callback_query(F.data == 'Опция 2')
async def op2(callback: CallbackQuery):
    await callback.message.answer('Это текст при нажатии инлайн кнопки Опция 2')


@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer('_____', reply_markup=kb.inline_keyboard_dynamic)


@dp.message(Command('links'))
async def links(message: Message):
    await message.answer('_____', reply_markup=kb.inline_keyboard_test)


@dp.message(F.text == "Привет")
async def test_button1(message: Message):
    name = message.from_user.first_name
    await message.answer(f'Привет! {name}')


@dp.message(F.text == "Пока")
async def test_button2(message: Message):
    name = message.from_user.first_name
    await message.answer(f'До свиданья, {name}')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
