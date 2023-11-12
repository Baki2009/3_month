from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token
import sqlite3

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Инициализация базы данных
conn = sqlite3.connect('bank_bot.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
''')
conn.commit()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Регистрация пользователя при первом использовании бота
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()

    await message.reply("Привет! Этот бот поможет вам управлять вашим банковским счетом. "
                        "Используйте команды /balance, /transfer, а для пополнения баланса используйте /deposit.")

@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    user_id = message.from_user.id

    cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    balance = result[0] if result else 0

    await message.reply(f"Ваш текущий баланс: {balance} сом." if result else "У вас еще нет счета. Используйте /start, чтобы зарегистрироваться.")

class Transfer(StatesGroup):
    user_id = State()
    summ = State()

@dp.message_handler(commands=['transfer'])
async def transfer_start(message: types.Message):
    await message.answer("Введите id пользователя, которому вы хотите сделать перевод:")
    await Transfer.user_id.set()

@dp.message_handler(state=Transfer.user_id)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer("Введите сумму, которую вы хотите перевести:")
    await Transfer.summ.set()

@dp.message_handler(state=Transfer.summ)
async def summm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get(Transfer.user_id)
    summ = float(data.get(Transfer.summ))

    try:
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (summ, user_id))
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (summ, message.from_user.id))
        conn.commit()

        await message.reply(f"Вы успешно перевели {summ} сом пользователю с id {user_id}!")

    except ValueError:
        await message.reply("Неверный формат суммы. Введите число.")
    finally:
        await state.finish()

@dp.message_handler(commands=['deposit'])
async def deposit_start(message: types.Message):
    await message.reply("Введите сумму для пополнения баланса:")
    dp.register_message_handler(deposit_amount, state='*')

async def deposit_amount(message: types.Message):
    amount = float(message.text)
    user_id = message.from_user.id

    # Выполнение пополнения баланса
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()

    await message.reply(f"Баланс успешно пополнен! Новый баланс: {amount} сом.")

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
