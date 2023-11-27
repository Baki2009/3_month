from config import token 
from aiogram import Bot, Dispatcher, types, executor, asyncio
import logging, aioschedule, schedule, requests
 
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}")

async def send_btc_price():
    url = "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url=url).json()
    price = round(float(response['price']), 3)
    await bot.send_message(-4091924505, f"BTC price {price} USD")

async def scheduler():
    aioschedule.every(10).seconds.do(send_btc_price)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(parametr):
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
