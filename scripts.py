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


async def checker():
    logging.info("Initialized checker")
    await asyncio.sleep(5*60)
    try:
        with MCRcon(host, password, port=port) as mcr:
            response = mcr.command("list").replace("There are ", "")[0]
            if response == "0":
                mcr.command("stop")
            else:
                asyncio.create_task(checker())
    except Exception as e:
        logging.info(e)


async def start():
    logging.info("Initialized start")
    subprocess.Popen('./start.sh', stdout=subprocess.PIPE)
    await checker()


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

checker()