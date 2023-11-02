# 1) Напишите телеграмм бот который загадывает случайное число с помощью
# библиотеки random и вы должны угадать его.
# Бот: Я загадал число от 1 до 3 угадайте
# Пользователь: Вводит число 2, если число правильное то выводит “Правильно вы
# отгадали”
# 2) Если пользователь выиграл отправляете данную фотографию
# https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg
# 3) Если пользователь проиграл, то отправляете данную фотографию
# https://media.makeameme.org/created/sorry-you-lose.jpg

from aiogram import Bot, Dispatcher, types, executor
from config import token
import random
import sys

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Я загадал число от 1 до 3 угадайте")
    await message.answer("Чтобы угадать число, отправь мне число от 1 до 3")
    await message.answer("После запуска можно продолжить играть не вводя /start!!! Что бы остановить введите команду /stop")

@dp.message_handler(commands=['stop'])
async def handle_stop(message: types.Message):
    await message.answer("Бот остановлен")
    sys.exit()

@dp.message_handler()
async def handle_message(message: types.Message):

    random_num = random.randint(1,3)
    user_message = int(message.text)

    try:
        user_message = int(message.text)
        if user_message == random_num:
            await message.answer_photo("https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg")
        elif user_message > 3:
            await message.answer("Загаданное число не может быть больше 3!!!")
        elif user_message < 1:
            await message.answer("Загаданное число не может быть меньше 1!!!")
        else:
            await message.answer_photo("https://media.makeameme.org/created/sorry-you-lose.jpg")

    except ValueError:
        await message.answer("Нужно ввести число, а не текст!!!")

executor.start_polling(dp)

# ДОП ЗАДАНИЕ:
# 4) Загрузить файлы в GitHub с .gitignore

