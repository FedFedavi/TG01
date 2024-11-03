import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile

from config import TOKEN
import sqlite3
import aiohttp
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()


init_db()


@dp.message(Command(commands=['show_records']))
async def show_records(message: Message):
    try:
        conn = sqlite3.connect('school_data.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM students')
        records = cur.fetchall()
        conn.close()

        if not records:
            await message.answer("В базе данных пока нет записей.")
            return

        response = "Записи в базе данных:\n"
        for record in records:
            response += f"ID: {record[0]}, Имя: {record[1]}, Возраст: {record[2]}, Класс: {record[3]}\n"

        await message.answer(response)

    except sqlite3.Error as e:
        await message.answer(f"Ошибка при получении записей из базы данных: {e}")

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Привет, как тебя зовут?')
    await state.set_state(Form.name)


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько тебе лет?')
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('В каком классе ты учишься?')
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data["name"], user_data["age"], user_data["grade"]))
    conn.commit()
    conn.close()

    await message.answer('Ок, записал')
    await show_records(message)
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
