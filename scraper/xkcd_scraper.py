import re
from json import JSONDecodeError

import requests

from xkcd import Xkcd

BASE_URL = "https://xkcd.com/{}/info.0.json"


def scrape(start, end):
    for comic_index in range(start, end + 1):
        comic = requests.get(BASE_URL.format(comic_index))
        try:
            json = comic.json()
            json["transcript"] = _cleanup(json["transcript"])
            yield to_xkcd(json)
        except JSONDecodeError:
            print("eek")


def _cleanup(text):
    """
    :param text: xkcd comic transciprt
    :return: cleaner version of the transcript stripped of evyerything but spaces + alphanumeric chars
    """
    return re.sub(r'([^\s\w]|_)+', '', text).replace('\n', '')


def to_xkcd(xkcd_json):
    return Xkcd(
        content=xkcd_json["transcript"],
        title=xkcd_json["title"],
        link=xkcd_json["img"],
        neighbors=[]
    )
