import asyncio
import logging
import subprocess
from os import getenv
from dotenv import load_dotenv


from mcrcon import MCRcon

load_dotenv()
# Параметры сервера
host = getenv("MC_HOST")
port = int(getenv("MC_PORT"))
password = getenv("MC_PASSWORD")


def start():
    logging.info("Initialized start")
    subprocess.Popen('./start.sh', stdout=subprocess.PIPE)


async def stop(delay: int = 60):
    logging.info(f"Initialized stop with {delay}sec delay")
    with MCRcon(host, password, port=port) as mcr:
        mcr.command(f"say server will stop after {delay}sec")
        await asyncio.sleep(delay)
        mcr.command("stop")


async def restart(delay: int = 60):
    logging.info(f"Initialized restart with {delay}sec delay")
    await stop(delay)
    start()


def say(text: str = "Hello!"):
    logging.info(f"Initialized say with {text} text")
    with MCRcon(host, password, port=port) as mcr:
        mcr.command(f"say {text}")
