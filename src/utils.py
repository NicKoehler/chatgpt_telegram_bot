import logging
import asyncio
from time import time
from random import choice
from os import name, system
from subprocess import run, PIPE
from aiogram import types, exceptions
from revChatGPT.ChatGPT import Chatbot
from internationalization import get_translation


logger = logging.getLogger("chatgpt_telegram_bot")
start_command = r".\start.ps1" if name == "nt" else "./start.sh"
pip_command = r".\venv\Scripts\pip" if name == "nt" else "./venv/bin/pip"


class Spinner:

    _all = [
        ["◐", "◓", "◑", "◒"],
        [".", "..", "...", ".."],
        ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
        ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
        ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
        ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔"],
        ["▉", "▊", "▋", "▌", "▍", "▎", "▏", "▎", "▍", "▌", "▋", "▊"],
        ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃"],
        ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"],
    ]

    def __init__(self) -> None:
        self.list = choice(self._all)
        self.length = len(self.list)
        self._curr = 0

    def get_next(self):
        s = self.list[self._curr]
        self._curr = (self._curr + 1) % self.length
        return s


async def spinner_maker(user_message: types.Message, condition: asyncio.Condition):

    spinner = Spinner()
    message = await user_message.answer(spinner.get_next())
    start_time = time()
    t1 = start_time
    while condition.locked() and t1 - start_time < 60 * 5:
        t2 = time()
        if t2 - t1 > 2:
            try:
                message = await message.edit_text(spinner.get_next())
                t1 = t2
            except exceptions.RetryAfter as e:
                await asyncio.sleep(e.timeout)
        await asyncio.sleep(0.1)
    await message.delete()


async def send_gpt_message(
    chatbot: Chatbot, message: types.Message, condition: asyncio.Condition
):
    loop = asyncio.get_event_loop()
    try:
        resp = await loop.run_in_executor(None, chatbot.ask, message.text)
    except Exception as e:
        resp = {"message": e}
    finally:
        condition.release()
        return resp


async def get_chatgpt_response(chatbot: Chatbot, message: types.Message):
    condition = asyncio.Condition()
    await condition.acquire()
    response = (
        await asyncio.gather(
            spinner_maker(message, condition),
            send_gpt_message(chatbot, message, condition),
        )
    )[1]

    return response or {"message": None}


async def update_and_restart(message: types.Message):
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


def stop_bot():
    asyncio.get_event_loop().stop()
