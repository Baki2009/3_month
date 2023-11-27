import asyncio
from aioschedule import every, run_every
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import token
bot = Bot(token=token)
dp = Dispatcher(bot)

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        await bot.send_message(-4091924505, "This message is sent every 10 seconds")

async def on_startup(dp):
    await bot.send_message(-4091924505, "Bot has been started")

if __name__ == '__main__':
    from aiogram import executor

    loop = asyncio.get_event_loop()
    
    # Запуск задачи с использованием run_every
    loop.create_task(run_every(scheduled, 10))

    # Запуск бота
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
