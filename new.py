from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token 
import sqlite3

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
# Импорт библиотек и настройка бота

conn = sqlite3.connect('bank_bot.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
''')
conn.commit()
# Подключение к базе данных и создание таблицы  

class TransferMoney(StatesGroup):
    amount = State()
    recipient = State()
# Определение состояний для машины состояний (FSM)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()

    await message.reply("Привет! Этот бот поможет вам управлять вашим банковским счетом. "
                        "Используйте команды /balance, /transfer и /deposit.")
# Обработка команды /start

@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    user_id = message.from_user.id

    cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        await message.reply(f"Ваш текущий баланс: {balance} сом.")
    else:
        await message.reply("У вас еще нет счета. Используйте /start, чтобы зарегистрироваться.")
# Обработка команды /balance

@dp.message_handler(commands=['transfer'])
async def transfer_start(message: types.Message):
    await message.reply("Введите сумму перевода:")
    await TransferMoney.amount.set()

@dp.message_handler(state=TransferMoney.amount)
async def transfer_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        user_id = message.from_user.id

        cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,))
        sender_balance = cursor.fetchone()[0]

        if sender_balance < amount:
            await message.reply("У вас недостаточно средств для перевода.")
            await state.finish()
            return

        await state.update_data(amount=amount)
        await message.reply("Введите ID получателя:")
        await TransferMoney.recipient.set()

    except ValueError:
        await message.reply("Неверный формат суммы. Введите число.")
        await state.finish()


@dp.message_handler(state=TransferMoney.recipient)
async def transfer_recipient(message: types.Message, state: FSMContext):
    try:
        recipient_id = int(message.text)
        data = await state.get_data()

        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (data['amount'], message.from_user.id))
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (data['amount'], recipient_id))
        conn.commit()

        await state.finish()
        await message.reply(f"Перевод успешно выполнен!")

    except ValueError:
        await message.reply("Неверный формат ID получателя. Введите число.")
        await state.finish()

@dp.message_handler(commands=['deposit'])
async def deposit_start(message: types.Message):
    await message.reply("Введите сумму для пополнения баланса:")
    dp.register_message_handler(deposit_amount, state='*')
# Обработка команды /transfer

async def deposit_amount(message: types.Message):
    try:
        amount = float(message.text)
        user_id = message.from_user.id

        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()

        await message.reply(f"Баланс успешно пополнен! Новый баланс: {amount} сом.")

    except ValueError:
        await message.reply("Неверный формат суммы. Введите число.")
# Обработка команды /deposit


if __name__ == '__main__':
    import asyncio
    from aiogram import executor

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(executor.start_polling(dp, skip_updates=True))
    finally:
        loop.run_until_complete(dp.storage.close())
        loop.run_until_complete(dp.storage.wait_closed())
        loop.close()
# Запуск бота. У меня все время выходила ошибка не понимал что с ней сделать вбил в chatgpt и вот что вышло