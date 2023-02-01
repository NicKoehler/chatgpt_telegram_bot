import asyncio
from time import time
from aiogram import types, exceptions
from revChatGPT.Official import Chatbot


async def send_message(s: str, message: types.Message) -> types.Message:
    while True:
        try:
            return await message.answer(s)
        except exceptions.CantParseEntities:
            return await message.answer(s, parse_mode=types.ParseMode.HTML)
        except exceptions.BadRequest:
            return
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)


async def edit_message(s: str, message: types.Message) -> types.Message:
    while True:
        try:
            await message.edit_text(s)
            break
        except exceptions.CantParseEntities:
            await message.edit_text(s, parse_mode=types.ParseMode.HTML)
            break
        except exceptions.MessageNotModified:
            break
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)


async def send_gpt_message(chatbot: Chatbot, message: types.Message):
    t1 = time()
    full_message = ""
    starting_message = None
    for response in chatbot.ask_stream(message.text):
        full_message += response
        if starting_message is None:
            starting_message = await send_message(full_message, message)
        elif time() - t1 >= 2:
            t1 = time()
            await edit_message(full_message, starting_message)

    if starting_message is not None and starting_message.text != full_message:
        await edit_message(full_message, starting_message)
