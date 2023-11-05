from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from config import token
import sqlite3

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)
connection = sqlite3.connect('itbot.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username VARCHAR(200),
        first_name VARCHAR(200),
        last_name VARCHAR(100)
    )
''')
cursor.execute("""
CREATE TABLE IF NOT EXISTS receipt(
    payment_code INT,
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    direction VARCHAR(200),
    amount INT,
    date VARCHAR(100)
);
""")
connection.commit()
connection.close()

start_buttons = {
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Контакты"),
    types.KeyboardButton("Курсы")
}
start_keybord = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.reply("Привет, Добро пожаловать в курсы Geeks!", reply_markup=start_keybord)
    
    user = message.from_user

    conn = sqlite3.connect('itbot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                   (user.id, user.username, user.first_name, user.last_name))
    conn.commit()
    conn.close()

@dp.message_handler(text="О нас")
async def about_us(message:types.Message):
    await message.answer("Geeks - это айти курсы в Бишкеке, Кара-Балте и Оше созданные в 2019 году")

@dp.message_handler(text="Адрес")
async def address(message:types.Message):
    await message.answer("Наш адрес:\nМырзалы Аматова 15 (БЦ Томирис)")
    await message.answer_location(40.51933983835417, 72.80298453971301)

@dp.message_handler(text="Контакты")
async def contacts(message:types.Message):
    await message.answer("Наши контакты:")
    await message.answer_contact("+996777123123", "Nurbolot", "Erkinbaev")
    await message.answer_contact("+996777123120", "Ulan", "Ashirov")

courses_buttons = {
    types.KeyboardButton("BackEnd"),
    types.KeyboardButton("FrontEnd"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Назад")
}
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)

@dp.message_handler(text = "Курсы")
async def courses(message:types.Message):
    await message.answer("Вот наши курсы:", reply_markup=courses_keyboard)

@dp.message_handler(text="BackEnd")
async def backend(message:types.Message):
    await message.answer("BackEnd - это серверная сторона приложения или сайта, которую мы не видим")

@dp.message_handler(text="FrontEnd")
async def frontend(message:types.Message):
    await message.answer("FrontEnd - это лицевая сторона сайта, которую мы можем видеть своими глазами")

@dp.message_handler(text="IOS")
async def ios(message:types.Message):
    await message.answer("IOS - это операционная система на мобильных устройствах компании Apple")

@dp.message_handler(text="Android")
async def android(message:types.Message):
    await message.answer("Android - это популярная опреационная система, которую используют многие компании")

@dp.message_handler(text="UX/UI")
async def uxui(message:types.Message):
    await message.answer("UX/Ui - это дизайн сайта или приложения")

@dp.message_handler(text="Назад")
async def cancell(message:types.Message):
    await start(message)

executor.start_polling(dp)

# Нужно собирать данные пользоваетля в таблицу users, при использовании команды /start. Если пользователь есть в таблице, то его не записывать . В случае если его нету, то записывать.