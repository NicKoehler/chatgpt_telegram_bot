#!venv/bin/python


import asyncio
import warnings
from dotenv import load_dotenv
from subprocess import run, PIPE
from os import getenv, name, system
from revChatGPT.ChatGPT import Chatbot
from utils import get_chatgpt_response
from aiogram.utils.exceptions import BotBlocked
from internationalization import get_translation
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

warnings.filterwarnings("ignore")

OWNER_ID = int(getenv("OWNER_ID"))
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
OPENAI_SESSION_TOKEN = getenv("OPENAI_SESSION_TOKEN")
OWNER_CHAT_FILTER = lambda message: message.chat.id == OWNER_ID

chatbot = Chatbot(config={"session_token": OPENAI_SESSION_TOKEN})
loop = asyncio.get_event_loop()
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


@dp.message_handler(OWNER_CHAT_FILTER, commands="start")
async def start_handler(message: types.Message):
    await message.answer(get_translation("start", message.from_user.language_code))


@dp.message_handler(OWNER_CHAT_FILTER, commands="rollback")
async def rollback_handler(message: types.Message):
    try:
        chatbot.rollback_conversation()
        await message.answer(
            get_translation("rollback_ok", message.from_user.language_code)
        )
    except IndexError:
        await message.answer(
            get_translation("rollback_fail", message.from_user.language_code)
        )


@dp.message_handler(OWNER_CHAT_FILTER, commands="reset")
async def reset_handler(message: types.Message):
    chatbot.reset_chat()
    await message.answer(get_translation("reset", message.from_user.language_code))


@dp.message_handler(OWNER_CHAT_FILTER, commands="stop")
async def stop_handler(message: types.Message):
    await message.answer(get_translation("stop", message.from_user.language_code))
    loop.stop()


@dp.message_handler(OWNER_CHAT_FILTER, commands="update")
async def update_handler(message: types.Message):
    await message.answer(
        get_translation("update_load", message.from_user.language_code)
    )
    p = run(["git", "pull"], stdout=PIPE, stderr=PIPE, text=True)
    if p.stdout:
        await message.answer(p.stdout)
    if p.stderr:
        await message.answer(p.stderr)
    await message.answer(
        get_translation("update_done", message.from_user.language_code)
    )
    system(r".\start.ps1" if name == "nt" else r".\start.sh")
    loop.stop()


@dp.message_handler(OWNER_CHAT_FILTER)
async def text_handler(message: types.Message):
    await message.answer_chat_action("typing")

    response = await get_chatgpt_response(chatbot, message)
    if response["message"]:
        try:
            await message.answer(response["message"])
        except:
            await message.answer(response["message"], parse_mode="HTML")
    else:
        await message.answer(get_translation("empty", message.from_user.language_code))


async def ready(_):
    try:
        await bot.send_message(OWNER_ID, "✅ • Online")
    except BotBlocked:
        pass


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=ready, skip_updates=True)
