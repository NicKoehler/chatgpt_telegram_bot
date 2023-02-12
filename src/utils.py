import logging
import asyncio
from time import time
from html import escape
from os import name, system
from subprocess import run, PIPE
from revChatGPT.V2 import Chatbot
from aiogram import types, exceptions
from internationalization import get_translation

logger = logging.getLogger("chatgpt_telegram_bot")
start_command = r".\start.ps1" if name == "nt" else "./start.sh"
pip_command = r".\venv\Scripts\pip" if name == "nt" else "./venv/bin/pip"


async def send_message(s: str, message: types.Message) -> types.Message | None:
    while True:
        try:
            return await message.answer(s)
        except exceptions.CantParseEntities:
            return await message.answer(escape(s), parse_mode=types.ParseMode.HTML)
        except exceptions.BadRequest:
            return
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)


async def edit_message(s: str, message: types.Message) -> None:
    while True:
        try:
            await message.edit_text(s)
            break
        except exceptions.CantParseEntities:
            try:
                await message.edit_text(escape(s), parse_mode=types.ParseMode.HTML)
                break
            except exceptions.MessageNotModified:
                break
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)


async def send_gpt_message(chatbot: Chatbot, message: types.Message) -> None:
    """
    send messages in parts updating the answer
    """

    t1 = time()
    full_message = ""
    starting_message = None
    async for line in chatbot.ask(message.text):
        if line["choices"][0]["finish_details"]:
            break
        full_message += line["choices"][0]["text"]
        if starting_message is None:
            starting_message = await send_message(full_message, message)
        elif time() - t1 >= 2:
            t1 = time()
            await edit_message(full_message, starting_message)

    if starting_message is not None and starting_message.text != full_message:
        await edit_message(full_message, starting_message)


async def update_and_restart(message: types.Message) -> None:
    """
    Pulls updates from github, updates the packages and restart the bot
    informing the user
    """
    await message.answer(
        get_translation("update_load", message.from_user.language_code)
    )
    p = run(["git", "pull"], stdout=PIPE, stderr=PIPE, text=True)
    if p.stdout:
        await message.answer(p.stdout)
    if p.stderr:
        await message.answer(p.stderr)
    p = run(
        [pip_command, "install", "-r", "requirements.txt", "--upgrade"],
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )
    if p.stdout:
        logger.info(p.stdout)
    if p.stderr:
        logger.error(p.stderr)
    await message.answer(
        get_translation("update_done", message.from_user.language_code)
    )
    system(start_command)
    stop_bot()


def stop_bot() -> None:
    """
    Stop the bot
    """
    asyncio.get_event_loop().stop()
