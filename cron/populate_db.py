import os

from scraper import xkcd_scraper
import requests
print(os.getenv("FOO"))
APP_ENDPOINT = "http://localhost:8000/insert"


def run(start, end):
    for xkcd_comic in xkcd_scraper.scrape(0, 4):
        requests.post(APP_ENDPOINT, json=xkcd_comic.to_dict())


run(0, 5)
