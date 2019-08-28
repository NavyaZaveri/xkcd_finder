import asyncio
from json import JSONDecodeError
import logging
import os
from pathlib import Path
import re
import socket
import time

import aiohttp
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

nltk.download("stopwords")
nltk.download("wordnet")

import requests
from models.xkcd import Xkcd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "https://xkcd.com/{}/info.0.json"
insert_endpoint = "http://localhost:8000/insert"
STOPOWRDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def cleanup(text):
    words = re.sub(r'([^\s\w]|_)+', '', text).replace('\n', '').split(" ")
    words_without_stopwords = [w.lower() for w in words if w not in STOPOWRDS]
    lemmatized = [lemmatizer.lemmatize(w) for w in words_without_stopwords]
    return " ".join(lemmatized)


def to_xkcd(xkcd_json):
    return Xkcd(
        content=xkcd_json["transcript"],
        title=xkcd_json["title"],
        link=xkcd_json["img"],
    )


from scraper.async_scheduler import AsyncScheduler


async def make_request(req_count, scheduler):
    if req_count == 200:
        return None
    await scheduler.add_task(make_request, req_count=req_count + 1)
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        verify_ssl=False,
    )
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            url = BASE_URL.format(req_count)
            xkcd = await fetch(session, url)
            await insert_into_db(session, xkcd)
            print(xkcd)
            print("done!")
        except Exception as e:
            print(e)


async def fetch(session, url):
    resp = await session.get(url)
    json = await resp.json()
    json["transcript"] = cleanup(json["transcript"])
    xkcd = to_xkcd(json)
    return xkcd


async def insert_into_db(session, xkcd):
    await session.post(insert_endpoint, json={
        "doc": xkcd.to_dict(),
        "password": os.environ.get("PASSWORD")
    })


if __name__ == "__main__":

    t = time.time()
    s = AsyncScheduler(wait=3)
    s.set_initial_callback(make_request, req_count=1)
    s.go()
    print(time.time() - t)
    print("--------------------")
    t = time.time()
    for i in range(1, 200):
        xkcd = requests.get("https://xkcd.com/1/info.0.json")
        json = xkcd.json()
        json["transcript"] = cleanup(json["transcript"])
        xkcd = to_xkcd(json)
        resp = requests.post(insert_endpoint, json={
            "doc": xkcd.to_dict(),
            "password": os.environ.get("PASSWORD")
        })
        print(resp.status_code, i)
    print(time.time() - t)
