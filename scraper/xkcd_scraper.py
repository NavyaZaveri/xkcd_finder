import logging
import re
from json import JSONDecodeError

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

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
