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
