import asyncio
import logging
import os
from pathlib import Path
import time

import aiohttp
from dotenv import load_dotenv
import requests

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from models.xkcd import Xkcd
from scraper.async_scheduler import AsyncRequestScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XkdcFetcher:
    def __init__(self):
        self.xkcd_list = []
        self.BASE_URL = "https://xkcd.com/{}/info.0.json"

    async def make_request(self, req_count, scheduler, session):
        if req_count == 10:
            return None
        await scheduler.add_task(self.make_request, req_count=req_count + 1)
        xkcd = await self.fetch(self.BASE_URL.format(req_count), session)
        async with asyncio.Lock():
            if xkcd is not None:
                self.xkcd_list.append(xkcd.to_dict())

    async def fetch(self, url, session):
        resp = await session.get(url)
        try:
            json = await resp.json()
            return Xkcd.from_json(json)
        except aiohttp.client_exceptions.ContentTypeError:
            pass


async def start():
    t = time.time()
    xf = XkdcFetcher()
    async with AsyncRequestScheduler(wait=5) as a:
        a.set_initial_callback(xf.make_request, req_count=1)
        await a.go()
    print(len(xf.xkcd_list))
    print(a.completed)
    print(time.time() - t)
    resp = requests.post("http://localhost:8000/bulk-insert", json={
        "docs": xf.xkcd_list,
        "password": os.environ["PASSWORD"]
    })
    print(resp.json())


def run_async_function():
    asyncio.run(start())


if __name__ == "__main__":
    run_async_function()
