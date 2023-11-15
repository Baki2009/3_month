import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для скачивания видео из TikTok. Просто отправь мне ссылку на видео.")

@dp.message_handler()
async def process_video(message: types.Message):
    input_url = message.text
    split_url = input_url.split("/")
    current_id = split_url[5].split("?")[0]

    video_api_url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}"
    video_api = requests.get(video_api_url).json()

    if 'aweme_list' in video_api:
        video_url = video_api['aweme_list'][0]['video']['play_addr']['url_list'][0]
        title = video_api['aweme_list'][0]['desc']

        try:
            os.mkdir('video')
        except FileExistsError:
            pass

        try:
            with open(f'video/{title}.mp4', 'wb') as video_file:
                video_file.write(requests.get(video_url).content)
            await message.reply(f"Видео {title}.mp4 успешно скачано в папку video", parse_mode=ParseMode.MARKDOWN)
        except Exception as error:
            await message.reply(f"Произошла ошибка при скачивании видео: {error}", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("Не удалось получить информацию о видео. Убедитесь, что ссылка правильная.")

executor.start_polling(dp, skip_updates=True)