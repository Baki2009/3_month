from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from config import token 
from bs4 import BeautifulSoup
import requests

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Здравствуйте! Добро пожаловать.")

@dp.message_handler(commands='phone')
async def parsing_and_send_phones(message:types.Message):
    await message.answer("Начинаю парсинг...")
    url = 'https://www.sulpak.kg/f/smartfoniy/osh/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_phones = soup.find_all('div', class_='product__item-name')
    all_prices = soup.find_all('div', class_='product__item-price')
    for name, price in zip(all_phones, all_prices):
        current_price = "".join(price.text.split())
        print(name.text, current_price)
        await message.answer(f"{name.text} {current_price}")

executor.start_polling(dp)