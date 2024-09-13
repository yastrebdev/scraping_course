import asyncio
import json
import time

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold, hlink

from main import collect_data

bot = Bot(token='6942157087:AAEXKSujr-Oy-PFiCsvc9Gal8GQe9tau_I4',
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

categories = ['ножи', 'перчатки', 'пистолеты', 'штурмовые винтовки']

keyboard_categories = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Ножи'), KeyboardButton(text='Перчатки')],
    [KeyboardButton(text='Пистолеты'), KeyboardButton(text='Штурмовые винтовки')],
], resize_keyboard=True)

keyboard_discount = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='от 10%'), KeyboardButton(text='от 20%'), KeyboardButton(text='от 30%'), KeyboardButton(text='от 40%')],
    [KeyboardButton(text='от 50%'), KeyboardButton(text='от 60%'), KeyboardButton(text='от 70%'), KeyboardButton(text='от 80%')],
], resize_keyboard=True)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text='Выберите категорию', reply_markup=keyboard_categories)


@dp.message()
async def echo(message: types.Message):
    msg = message.text.lower()

    if msg in categories:
        await message.answer(text='Пожалуйста подождите...')

        collect_data(category=msg, discount=50)

        with open('data.json') as file:
            data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item['full_name'], item['3d_link'] if item['3d_link'] != 'Нет ссылки' else None)}\n' \
                f'{hbold('ID: ')}{item['id']}\n' \
                f'{hbold('Цена: ')}{item['price']}$\n' \
                f'{hbold('Скидка: ')}{item['discount']}% 🔥'

            if index % 5 == 0:
                time.sleep(10)

            await message.answer(card)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())