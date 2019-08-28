from abc import ABC
import asyncio
import logging
import re
from json import JSONDecodeError
import os

from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import aiohttp
from pathlib import Path

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

nltk.download("stopwords")
nltk.download("wordnet")
from scraper.async_scraper import  schedule_request

import requests
from models.xkcd import Xkcd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "https://xkcd.com/{}/info.0.json"
STOPOWRDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def cleanup(text):
    words = re.sub(r'([^\s\w]|_)+', '', text).replace('\n', '').split(" ")
    words_without_stopwords = [w.lower() for w in words if w not in STOPOWRDS]
    lemmatized = [lemmatizer.lemmatize(w) for w in words_without_stopwords]
    return " ".join(lemmatized)


def scrape(start, end):
    for comic_index in range(start, end + 1):
        url = BASE_URL.format(comic_index)
        comic = requests.get(url)
        try:
            json = comic.json()
            json["transcript"] = cleanup(json["transcript"])
            yield to_xkcd(json)
        except JSONDecodeError as e:
            logging.info(
                f"unable to scrape {url}: {e}"
            )


def to_xkcd(xkcd_json):
    return Xkcd(
        content=xkcd_json["transcript"],
        title=xkcd_json["title"],
        link=xkcd_json["img"],
    )


class XkcdRequest:
    def __init__(self, verbose=True):
        self.insert_endpoint = "http://localhost:8000/insert"
        self.scraper_url = "https://xkcd.com/{}/info.0.json"
        self.verbose = verbose
        self.retry_list = []
        self.seen = set()

    async def make_request(self, session, req_count):
        try:
            await asyncio.sleep(0.5)
            xkcd = await self.fetch(session, req_count)
            await asyncio.sleep(0.5)
            await self.insert_into_db(session, xkcd)
            await asyncio.sleep(0.5)
            lock = asyncio.Lock()
            print("done")
            async with lock:
                self.seen.add(xkcd)
        except aiohttp.client_exceptions.ContentTypeError as e:
            print(e)
        except aiohttp.client_exceptions.ClientOSError:
            self.retry_list.append(req_count)

    async def fetch(self, session, req_count):
        print(self.scraper_url.format(req_count), req_count)

        resp = await session.get(self.scraper_url.format(req_count))
        json = await resp.json()
        json["transcript"] = cleanup(json["transcript"])
        xkcd = to_xkcd(json)
        return xkcd

    async def insert_into_db(self, session, xkcd):
        await session.post(self.insert_endpoint, json={
            "doc": xkcd.to_dict(),
            "password": os.environ.get("PASSWORD")
        })


if __name__ == "__main__":
    x = XkcdRequest()
    schedule_request(x.make_request, 20)
