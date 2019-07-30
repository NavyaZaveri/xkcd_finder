import os

import requests
from dotenv import load_dotenv

from scraper import xkcd_scraper

load_dotenv()

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
APP_ENDPOINT = "http://localhost:8000/insert"


def run(start, end):
    for xkcd_comic in xkcd_scraper.scrape(0, end):
        requests.post(APP_ENDPOINT, json={
            "doc": xkcd_comic.to_dict(),
            "password": os.environ("PASSWORD")
        })


run(0, 10)
