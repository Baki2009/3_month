# Описание:
# Сделать ToDo List Bot (Список дел) с использованием библиотек aiogram
# Пользователь:
# Пользователь может добавлять список своих дел (title, datetime) и данные должны
# попасть в базу данных
# И также пользователь может удалять свои дела из нашей базы данных
# ДОП ЗАДАНИЕ:
# Использовать inline кнопки
# Загрузить код в GitHub c .gitignore

from config import token
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

delete = MemoryStorage()
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todo(
    title TEXT,
    date_time TEXT
);
""")
conn.commit()

class TodoStates(StatesGroup):
    title = State()
    datetime = State()
    delete = State()


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Этот бот поможет тебе вести список дел. Используй /add для добавления задачи.")


@dp.message_handler(Command("add"))
async def cmd_add(message: types.Message):
    await message.answer("Введите заголовок задачи:")
    await TodoStates.title.set()

@dp.message_handler(state=TodoStates.title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите дату и время выполнения задачи в формате YYYY-MM-DD HH:MM:")
    await TodoStates.datetime.set()

@dp.message_handler(state=TodoStates.datetime)
async def process_datetime(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    datetime_str = message.text

    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todo (title, date_time) VALUES (?, ?)', (title, datetime_str))
        conn.commit()
        conn.close()

        await message.answer(f"Задача '{title}' добавлена в список дел на {datetime_str}.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await state.finish()


@dp.message_handler(Command("list"))
async def cmd_list(message: types.Message):
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('SELECT title, date_time FROM todo')
        tasks = cursor.fetchall()
        conn.close()

        if tasks:
            task_list = "\n".join([f"{title} - {datetime}" for title, datetime in tasks])
            await message.answer(f"Список дел:\n{task_list}")
        else:
            await message.answer("Список дел пуст.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@dp.message_handler(Command("delete"))
async def delete(message: types.Message):
    await message.answer("Введите заголовок задачи, которую вы хотите удалить:")
    await TodoStates.delete.set()

@dp.message_handler(state=TodoStates.delete)
async def dellete(message: types.Message, state: FSMContext):
    delete_title = message.text

    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todo WHERE title=?', (delete_title,))
        conn.commit()
        conn.close()

        await message.answer(f"Задача '{delete_title}' удалена из списка дел.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await state.finish() 


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
