#!venv/bin/python

import warnings
from os import getenv
from dotenv import load_dotenv
from revChatGPT.Official import Chatbot
from aiogram.utils.exceptions import BotBlocked
from internationalization import get_translation
from aiogram import Bot, Dispatcher, executor, types
from utils import send_gpt_message, update_and_restart, stop_bot

load_dotenv()

warnings.filterwarnings("ignore")

OWNER_ID = int(getenv("OWNER_ID"))
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
OWNER_CHAT_FILTER = lambda message: message.chat.id == OWNER_ID

chatbot = Chatbot(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


@dp.message_handler(OWNER_CHAT_FILTER, commands="start")
async def start_handler(message: types.Message):
    await message.answer(get_translation("start", message.from_user.language_code))


@dp.message_handler(OWNER_CHAT_FILTER, commands="rollback")
async def rollback_handler(message: types.Message):
    try:
        chatbot.rollback(1)
        await message.answer(
            get_translation("rollback_ok", message.from_user.language_code)
        )
    except IndexError:
        await message.answer(
            get_translation("rollback_fail", message.from_user.language_code)
        )


@dp.message_handler(OWNER_CHAT_FILTER, commands="reset")
async def reset_handler(message: types.Message):
    chatbot.reset()
    await message.answer(get_translation("reset", message.from_user.language_code))


@dp.message_handler(OWNER_CHAT_FILTER, commands="stop")
async def stop_handler(message: types.Message):
    await message.answer(get_translation("stop", message.from_user.language_code))
    stop_bot()


@dp.message_handler(OWNER_CHAT_FILTER, commands="update")
async def update_handler(message: types.Message):
    await update_and_restart(message)


@dp.message_handler(OWNER_CHAT_FILTER)
async def text_handler(message: types.Message):
    await message.answer_chat_action("typing")
    await send_gpt_message(chatbot, message)


async def ready(_):
    try:
        await bot.send_message(OWNER_ID, "✅ • Online")
    except BotBlocked:
        pass


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=ready, skip_updates=True)
