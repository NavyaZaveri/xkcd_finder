import asyncio
import logging
import os
from pathlib import Path
import time

from dotenv import load_dotenv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from models.xkcd import Xkcd
from scraper.async_scheduler import AsyncRequestScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "https://xkcd.com/{}/info.0.json"
insert_endpoint = "http://localhost:8000/insert"


async def make_request(req_count, scheduler, session):
    if req_count == 200:
        return None

    await scheduler.add_task(make_request, req_count=req_count + 1)
    url = BASE_URL.format(req_count)
    xkcd = await fetch(url, session)
    await insert_into_db(xkcd, session=session)
    print(xkcd)
    print("done!")


async def fetch(url, session):
    resp = await session.get(url)
    json = await resp.json()
    return Xkcd.from_json(json)


async def insert_into_db(xkcd, session):
    await session.post(insert_endpoint, json={
        "doc": xkcd.to_dict(),
        "password": os.environ.get("PASSWORD")
    })


async def start():
    t = time.time()
    async with AsyncRequestScheduler(wait=5) as a:
        a.set_initial_callback(make_request, req_count=1)
        await a.go()
    print(time.time() - t)
    print(a.completed)


def run_async_function():
    asyncio.run(start())


if __name__ == "__main__":
    run_async_function()
