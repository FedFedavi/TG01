from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Привет'), KeyboardButton(text='Пока')]
], resize_keyboard=True)


inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новости', url='https://newdaynews.ru/allnews/')],
    [InlineKeyboardButton(text='Музыка', url='https://zvuk.com/playlist/1062105/')],
    [InlineKeyboardButton(text='Видео', url='https://video-preview.s3.yandex.net/OjEsUgIAAAA.mp4')]
])

inline_keyboard_op = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Опция 1', callback_data='Опция 1')],
    [InlineKeyboardButton(text='Опция 2', callback_data='Опция 2')]
])

inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать больше', callback_data='view')]
])



test = ['Кнопка 1', 'Кнопка 2', 'Кнопка 3', 'Кнопка 4']


async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://video-preview.s3.yandex.net/AwH5LAEAAAA.mp4'))
    return keyboard.adjust(2).as_markup()
