#!venv/bin/python

import warnings
from os import getenv
from dotenv import load_dotenv
from revChatGPT.V2 import Chatbot
from aiogram.utils.exceptions import BotBlocked
from internationalization import get_translation
from aiogram import Bot, Dispatcher, executor, types
from utils import send_gpt_message, update_and_restart, stop_bot

load_dotenv()

warnings.filterwarnings("ignore")

PASS = getenv("PASS")
EMAIL = getenv("EMAIL")
OWNER_ID = int(getenv("OWNER_ID"))
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_IDS = set([OWNER_ID])
if allowed_ids := getenv("ALLOWED_IDS"):
    ALLOWED_IDS = ALLOWED_IDS.union(set(map(int, allowed_ids.split(","))))
OWNER_CHAT_FILTER = lambda message: message.chat.id == OWNER_ID
ALLOWED_CHAT_FILTER = lambda message: message.chat.id in ALLOWED_IDS

chatbots = {id: Chatbot(email=EMAIL, password=PASS) for id in ALLOWED_IDS}
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


@dp.message_handler(ALLOWED_CHAT_FILTER, commands="start")
async def start_handler(message: types.Message):
    await message.answer(get_translation("start", message.from_user.language_code))


@dp.message_handler(ALLOWED_CHAT_FILTER, commands="rollback")
async def rollback_handler(message: types.Message):
    chatbots[message.chat.id].conversations.rollback("default")
    await message.answer(get_translation("rollback", message.from_user.language_code))


@dp.message_handler(ALLOWED_CHAT_FILTER, commands="reset")
async def reset_handler(message: types.Message):
    chatbots[message.chat.id].conversations.remove("default")
    await message.answer(get_translation("reset", message.from_user.language_code))


@dp.message_handler(OWNER_CHAT_FILTER, commands="stop")
async def stop_handler(message: types.Message):
    await message.answer(get_translation("stop", message.from_user.language_code))
    stop_bot()


@dp.message_handler(OWNER_CHAT_FILTER, commands="update")
async def update_handler(message: types.Message):
    await update_and_restart(message)


@dp.message_handler(ALLOWED_CHAT_FILTER)
async def text_handler(message: types.Message):
    await message.answer_chat_action("typing")
    await send_gpt_message(chatbots[message.chat.id], message)


async def ready(_):
    try:
        await bot.send_message(OWNER_ID, "✅ • Online")
    except BotBlocked:
        pass


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=ready, skip_updates=True)
