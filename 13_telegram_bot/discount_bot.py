import asyncio
import json
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold, hlink
from aiogram.client.default import DefaultBotProperties

from main import collect_data

bot = Bot(token='6962547342:AAFl3tBLfZMCZ6hhyJU6H7eaE05SYk2YuSw',
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Кроссовки')],
        [KeyboardButton(text='Видеокарты')],
    ], resize_keyboard=True)

    await message.answer(text='Товары со скидкой!', reply_markup=keyboard)


@dp.message()
async def echo(message: types.Message):
    msg = message.text.lower()

    if msg == 'кроссовки':
        await message.answer(text='Please waiting...')

        collect_data()

        with open('shoes.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            card = f'{hlink(item['title'], item['url'])}\n' \
                f'{hbold('Бренд: ')}{item['brand']}\n' \
                f'{hbold('Цена: ')}{item['base_price']}\n' \
                f'{hbold('Цена со скидкой: ')}{item['discount_price']}🔥'

            await message.answer(card)
            time.sleep(5)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())