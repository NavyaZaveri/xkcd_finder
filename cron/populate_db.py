import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from scraper import xkcd_scraper

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

APP_ENDPOINT = "http://localhost:8000/insert"


def insert_comic(xkcd_comic):
    response = requests.post(APP_ENDPOINT, json={
        "doc": xkcd_comic.to_dict(),
        "password": os.environ.get("PASSWORD")
    })
    if response.status_code == 201:
        print("created")


def run(start, end):
    for xkcd_comic in xkcd_scraper.scrape(start, end):
        insert_comic(xkcd_comic)


# handle with arg-parse
run(0, 50)
