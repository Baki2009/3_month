import asyncio
import logging
import pymysql
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from config import token

db = pymysql.connect(host='localhost', user='your_user', password='your_password', database='your_db')
cursor = db.cursor()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет! Я бот о ресторане Ojak Kebab. Выберите действие:", reply_markup=menu_markup)


menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
menu_markup.add("Меню", "О нас", "Адрес", "Заказать еду")

from aiogram import executor
loop = asyncio.get_event_loop()
executor.start_polling(dp, skip_updates=True)

# ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
        # if text == str: ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            # cursor.execute("INSERT INTO food (name) VALUES (?)", (text))
            # await message.answer("Введите номер телефона:")
        # elif text == int:
        #     cursor.execute("INSERT INTO food (number) VALUES (?)", (text))
        #     await message.answer("Введите адрес доставки:")
        # elif text == tuple:
        #     cursor.execute("INSERT INTO food (delivery_address) VALUES (?)", (text))
        #     await message.answer("Вы успешно взяли заказ! Ждите доставку")
