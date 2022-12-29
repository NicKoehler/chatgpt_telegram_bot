import asyncio
from time import time
from random import choice
from aiogram import types, exceptions
from revChatGPT.ChatGPT import Chatbot


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


async def spinner_maker(user_message: types.Message, l: list[bool]):

    spinner = Spinner()
    message = await user_message.answer(spinner.get_next())
    start_time = time()
    t1 = start_time
    while l and t1 - start_time < 120:
        t2 = time()
        if t2 - t1 > 2:
            try:
                message = await message.edit_text(spinner.get_next())
                t1 = t2
            except exceptions.RetryAfter as e:
                await asyncio.sleep(e.timeout)
        asyncio.sleep(0.1)
    await message.delete()


async def send_gpt_message(chatbot: Chatbot, message: types.Message, l: list[bool]):
    loop = asyncio.get_event_loop()
    try:
        resp = await loop.run_in_executor(None, chatbot.ask, message.text)
    except Exception as e:
        resp = {"message": e}
    finally:
        l.pop()
        return resp


async def get_chatgpt_response(chatbot: Chatbot, message: types.Message):
    # please god forgive me
    l = set([0])
    response = (
        await asyncio.gather(
            spinner_maker(message, l), send_gpt_message(chatbot, message, l)
        )
    )[1]

    return response
