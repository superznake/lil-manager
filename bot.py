import asyncio
import logging
import sys
from os import getenv
from typing import Dict

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

import scripts

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
PASSWORD: str = getenv("PASSWORD")

users: Dict[int, str] = {0: "0"}

started = None

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

dp = Dispatcher()


@dp.message(F.text)
async def base_handler(message: Message):
    global users
    global PASSWORD
    global started
    logging.info(f"received message '{message.text}' from {message.from_user.username}| time: {message.date}")
    state = users.get(message.chat.id)
    match state:
        case "start":
            match message.text.lower():
                case "admin":
                    users[message.chat.id] = "login"
                    await message.answer(text="So give me a password, Admin!")
                case "user":
                    users[message.chat.id] = "user"
                    await message.answer(text="Hello, user! Instruction is here: http://superznake.ru/minecraft/how")
                case _:
                    await message.answer(text="Sorry, i don't know (")

        case "login":
            match message.text:
                case "back":
                    users[message.chat.id] = "start"
                    await message.answer(text="Hello, who are you?")
                case _:
                    if message.text == PASSWORD:
                        users[message.chat.id] = "admin"
                        await message.answer(text="Hello, Admin! Your commands: \n\n"
                                                  "/launch - start the server\n"
                                                  "/restart [t (optional, default: 60)] - "
                                                  "restarts server after t sec delay"
                                                  "\n/stop [t (optional, default: 60)] - "
                                                  "restarts server after t sec delay"
                                                  "\n/say [message optional, default:Hello] - "
                                                  "sends message in chat")
                    else:
                        await message.answer(text="Wrong password!")

        case "admin":
            match message.text:
                case "back":
                    users[message.chat.id] = "start"
                    await message.answer(text="Hello, who are you?")
                case "/launch":
                    if started is None or started.done():
                        started = asyncio.create_task(scripts.start())
                        await message.answer(text="Starting...")
                    else:
                        await message.answer(text="Server is running already")
                case _:
                    if message.text.startswith("/restart"):
                        if len(message.text) > len("/restart"):
                            delay = message.text.replace("/restart ", "")
                            if delay.isdigit():
                                delay = int(delay)
                                asyncio.create_task(scripts.restart(delay=delay))
                                await message.answer(text=f"Restart in {delay} sec")
                            else:
                                await message.answer(text="Error! Check your command.")
                        else:
                            asyncio.create_task(scripts.restart())
                            await message.answer(text="Restart in 60 sec")
                    elif message.text.startswith("/stop"):
                        if len(message.text) > len("/stop"):
                            delay = message.text.replace("/stop ", "")
                            if delay.isdigit():
                                delay = int(delay)
                                asyncio.create_task(scripts.stop(delay=delay))
                                await message.answer(text=f"Stop in {delay} sec")
                            else:
                                await message.answer(text="Error! Check your command.")
                        else:
                            asyncio.create_task(scripts.stop())
                            await message.answer(text="Stop in 60 sec")
                    elif message.text.startswith("/say"):
                        if len(message.text) > len("/say"):
                            text = message.text.replace("/say ", "")
                            scripts.say(text=text)
                            await message.answer(text=f"Said: {text}")
                        else:
                            scripts.say()
                            await message.answer(text="Said: Hello")
                    else:
                        await message.answer(text="Wrong command")

        case "user":
            match message.text:
                case "back":
                    users[message.chat.id] = "start"
                    await message.answer(text="Hello, who are you?")
                case "/launch":
                    if started is None or started.done():
                        started = asyncio.create_task(scripts.start())
                        await message.answer(text="Starting...")
                    else:
                        await message.answer(text="Server is running already")
                case _:
                    await message.answer(text="Wrong command")
        case _:
            users[message.chat.id] = "start"
            await message.answer(text="Hello, who are you?")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    print("running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
