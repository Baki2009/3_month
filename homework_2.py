# Напишите телеграмм бот для ojak kebab.
# Цель телеграмм бота выдавать информацию о заведении (меню, о нас, адрес,
# заказать еду)
# Сделайте кнопки (меню, о нас, адрес, заказать еду)
# И также сделайте так при нажатии кнопки запустить чтобы данные пользователей
# сохранились в базу данных (id, username, first_name, last_name, date_joined)
# При нажатии кнопки меню, пусть ему отправляются меню из этого сайта
# https://nambafood.kg/ojak-kebap (раздел шашлыки)
# При нажатии кнопки о нас, пусть ему отправится информация с сайта
# https://ocak.uds.app/c/about
# При нажатии кнопки адрес, пусть ему отправится информация об адресе заведения
# И также при нажатии кнопки заказать еду, то вы должны у пользователя запросить
# данные как имя, номер телефона, адрес доставки и также после получения данных
# записать в базу данных
# ДОП ЗАДАНИЕ:
# Загрузить код в GitHub и не забудьте использовать файл .gitignore

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging import basicConfig, INFO
import sqlite3
from datetime import datetime
from config import token

storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

connection = sqlite3.connect("ojak_kebab.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY, 
        username VARCHAR(200),
        first_name VARCHAR(200),
        last_name VARCHAR(200),
        date_joined VARCHAR(200)
);
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS food(
        name TEXT,
        number TEXT,
        delivery_address TEXT
);
''')

connection.commit()
connection.close()

start_buttons = {
    types.KeyboardButton("Меню"),
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Заказать еду")
}
start_keybord = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands = "start")
async def start(message:types.Message):
    await message.answer("Добро пожаловать в телеграмм бот ОЖАК КЕБАБ", reply_markup=start_keybord)

    user = message.from_user

    connection = sqlite3.connect('ojak_kebab.db')
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username, first_name, last_name, date_joined) VALUES (?, ?, ?, ?, ?)",
                   (user.id, user.username, user.first_name, user.last_name, message.date))
    connection.commit()
    connection.close()

@dp.message_handler(text = "Меню")
async def menu(message:types.Message):
    await message.answer("""Вот меню нашего кафе: \n Вали кебаб на 4 человек - 3200 сом \n Шефим кебаб - 420 сом \n Симит кебаб - 420 сом \n Форель на мангале целиком - 700 сом \n Адана с йогуртом - 420 сом \n Киремите кофте - 400 сом \n Патлышкан кебаб - 480 сом \n Ассорти кебаб (1 персона) - 480 сом \n Ассорти кебаб (1 персона) - 700 сом \n Крылышки на мангале - 400 сом \n Фыстыклы кебаб - 460 сом \n Чоп шиш баранина - 400 сом \n Перзола - 700 сом \n Сач кавурма с мясом - 450 сом \n Сач кавурма с курицей 440 сом \n Форель на мангале кусочками - 1100 сом \n Семга с ризотто - 800 сом \n Донер кебаб - 440 сом \n Донер сарма - 450 сом \n Шашлык из баранины - 450 сом \n Кашарлы кофте - 420 сом \n Ызгара кофте - 400 сом \n Урфа - 420 сом \n Адана острый - 420 сом \n Адана кебаб - 420 сом """)

@dp.message_handler(text = "О нас")
async def about_us(message:types.Message):
    await message.answer("""Ocak Kebap
\nКафе "Ожак Кебап" на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом.
\nНаше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.
\nВ 2016 году по голосованию на сайте "Horeca" были удостоены "Лучшее кафе на каждый день" и мы стараемся оправдать доверие наших гостей.
\nМы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е». У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции. Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.""")

@dp.message_handler(text = "Адрес")
async def addres(message:types.Message):
    await message.answer("Курманжан датка, 209")
    await message.answer_location(40.526504, 72.795442)

class OrderFoodState(StatesGroup):
    name = State()
    number = State()
    delivery_address = State()

@dp.message_handler(text='Заказать еду')
async def about(message:types.Message):
    await message.answer('Введите ваше имя')
    await OrderFoodState.name.set()

@dp.message_handler(state=OrderFoodState.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer("Введите свой номер телефона")
    await OrderFoodState.next()

@dp.message_handler(state=OrderFoodState.number)
async def number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text

    await message.answer("Введите свой адрес")
    await OrderFoodState.next()

@dp.message_handler(state=OrderFoodState.delivery_address)
async def address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_address'] = message.text

    async with state.proxy() as data:
        name = data['name']
        number = data['number']
        delivery_address = data['delivery_address']

    connection = sqlite3.connect("ojak_kebab.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO food (name, number, delivery_address )
        VALUES (?, ?, ?)
    ''', (name, number, delivery_address))
    connection.commit()

    await message.answer("Ваш заказ принять.\nЖдите он никогда не приедет")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
