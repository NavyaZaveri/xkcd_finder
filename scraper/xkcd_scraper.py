import string

import requests
import re

from es_api.client import Xkcd

BASE_URL = "https://xkcd.com/{}/info.0.json"


def scrape(start, end):
    for comic_index in range(start, end + 1):
        comic = requests.get(BASE_URL.format(comic_index))
        json = comic.json()
        json["transcript"] = _cleanup(json["transcript"])
        x = to_xkcd(json)
        print(x)


def _cleanup(text):
    """

    :param text: xkcd comic transciprt
    :return: cleaner version of the transcript stripped of evyerything but spaces + alphanumeric chars
    """
    return re.sub(r'([^\s\w]|_)+', '', text)


import uuid


def to_xkcd(xkcd_json):
    return Xkcd(
        id=uuid.uuid4(),
        content=xkcd_json["transcript"],
        title=xkcd_json["title"],
        link=xkcd_json["img"],
        neighbors=[]
    )


scrape(2, 5)
