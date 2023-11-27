# Описание:
# Сделать телеграм бота для обмена валюты
# Данные должны быть спарсены с сайта НАЦбанка (USD, EURO, RUB, KZT)
# https://www.nbkr.kg/index.jsp?lang=RUS
# Пользователь:
# Пользователь пишет боту и выбирает валюту которую нужно поменять,
# например KGS на USD и вы пишете 100 и получаете 8572 сом (примерно по
# курсу валюты)
# ДОП ЗАДАНИЕ:
# Попробуйте сделать бота с использованием inline кнопок
# Загрузить код в GitHub с .gitignore

import logging
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import token 

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

NBKR_URL = 'https://www.nbkr.kg/index.jsp?lang=RUS'


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для обмена валют. Введите /exchange для начала обмена.")


@dp.message_handler(commands=['exchange'])
async def exchange_command(message: types.Message):
    await message.reply("Выберите валюту для обмена, например, KGS на USD.")


@dp.message_handler(lambda message: message.text() in ['USD', 'EURO', 'RUB', 'KGS'])
async def handle_currency(message: types.Message):
    try:
        currency_from = message.text.upper()

        # Парсим данные с сайта НБКР
        response = requests.get(NBKR_URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим курс валюты
        rate = float(soup.find('div', {'class': currency_from.lower()}).text)

        await message.reply(f"Введите сумму в {currency_from}:")
        await bot.register_next_step_handler(message, lambda msg: handle_amount(msg, rate))

    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")


async def handle_amount(message: types.Message, rate: float):
    try:
        amount = float(message.text)
        result = amount / rate
        await message.reply(f"{amount} {message.text.split()[1]} равны примерно {result:.2f} сом.")
    except ValueError:
        await message.reply("Введите корректное число.")


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
