from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging import basicConfig, INFO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from config import token
import sqlite3, uuid, time, os, sys
# Это все импорты которые нужны для корректной работы кода

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)
# Здесь я подключаю бота 

connection = sqlite3.connect('bank.db')
cursor = connection.cursor()
# Здесь я подключаю sqlite что бы создать базу данных

class bank(StatesGroup):
    name = State()
    surname = State()
    cash_account = State()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        name VARCHAR(200),
        surname VARCHAR(200), 
        cash_account VARCHAR(200)   
);
''')

cursor.execute("SELECT * FROM users WHERE name and surname")

connection.commit()
# Это база данных где будут хранится данные пользователей

# Это все регистрация

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer("""Наш позволяет пользователям проверять баланс своего
банковского счета, а также совершать переводы между счетами.""")
# Это команда /start

@dp.message_handler(commands="balance")
async def balance(message:types.Message):
    await message.answer("Вы должны войти систему. Введите свое имя:")

@dp.message_handler()
async def balance_name(message:types.Message, state:FSMContext):
    name = cursor.execute("SELECT * FROM users")
    surname = cursor.execute("SELECT * FROM users")

    if message.text in name:
        await message.answer("Теперь введите свою фамилию")
    elif message.text in surname:
        await message.answer(f"На вашем балансе {cash_account} сом")

@dp.message_handler(commands="register")
async def get_receipt(message:types.Message):
    await message.answer("Введите свое имя:")
    await bank.name.set()

@dp.message_handler(state=bank.name)
async def name(message:types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите свою фамилию:")
    await bank.surname.set()

@dp.message_handler(state=bank.surname)
async def surname(message:types.Message, state:FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите начальный пополнение:")
    await bank.cash_account.set()

@dp.message_handler(state=bank.cash_account)
async def cash_account(message:types.Message, state:FSMContext):
    await state.update_data(cash_account=message.text)
    result = await storage.get_data(user=message.from_user.id)
    print(result)
    cursor.execute(f"""INSERT INTO users (name, surname, cash_account)
                   VALUES (?, ?, ?);""", 
                   (result['name'], result['surname'], result['cash_account']))
    connection.commit()
    await message.answer("Вы успешно зарегистрировались!!!")

executor.start_polling(dp, skip_updates=True)

# Название проекта: Телеграм-бот для банковской системы
# Цель проекта:
# Разработать бота, который позволяет пользователям проверять баланс своего
# банковского счета, а также совершать переводы между счетами.
# Функциональные требования:
# 1. Регистрация и идентификация пользователя:
# - Бот должен иметь механизм регистрации и идентификации пользователей.
# - Используйте уникальные идентификаторы для каждого пользователя.
# 2. Команда /start:
# - Бот должен реагировать на команду /start, предоставляя пользователю краткую
# информацию о функциональности бота.
# 3. Команда /balance:
# - Бот должен реагировать на команду /balance, выводя текущий баланс
# пользователя.
# - В случае отсутствия у пользователя счета, бот должен информировать
# пользователя о необходимости создания счета.
# 4. Команда /transfer:
# - Бот должен реагировать на команду /transfer, предлагая пользователю ввести сумму
# перевода.
# - После ввода суммы бот должен запрашивать данные получателя (например, ID
# пользователя или номер счета).
# 5. Перевод средств:
# - Бот должен обрабатывать запросы на перевод средств между счетами.
# - При успешном переводе бот должен уведомлять отправителя и получателя о
# проведенной операции.
# 6. Безопасность:
# - Реализовать меры безопасности, такие как защита от SQL-инъекций и других видов
# атак.
# 7. Логирование:
# - Реализовать систему логирования для отслеживания ключевых операций и ошибок.
# Технические требования:
# 1. Использование библиотеки aiogram:
# - Реализовать бота с использованием библиотеки aiogram.
# 2. Хранение данных:
# - Использовать библиотеку sqlite3 для хранения данных пользователей и переводов
# денег.
# 3. Обработка ошибок:
# - Реализовать обработку возможных ошибок и уведомление пользователей о них.
# 4. Документация кода:
# - Предоставить подробный комментарий к коду для облегчения понимания его логики
# и функциональности.
# 5. Тестирование:
# - Провести тестирование бота на различных сценариях использования, включая
# проверку баланса и совершение переводов.
