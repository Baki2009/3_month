import sqlite3
from aiogram import Bot, Dispatcher, types, executor


from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)


# Создайте базу данных SQLite и таблицу, если они еще не существуют
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')
conn.commit()
conn.close()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    conn = sqlite3.connect('itbot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                   (user.id, user.username, user.first_name, user.last_name))
    conn.commit()
    conn.close()

    await message.reply("Информация о вас была сохранена в базе данных.")

executor.start_polling(dp)
