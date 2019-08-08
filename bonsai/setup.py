import os
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def _get_header(url):
    bonsai_url = 'https://366jcemnlk:t72d4o8zqy@xkcd-app-6996876562.ap-southeast-2.bonsaisearch.net'
    auth = re.search('https\:\/\/(.*)\@', bonsai_url).group(1).split(':')
    host = bonsai_url.replace('https://%s:%s@' % (auth[0], auth[1]), '')
    return [{
        'host': host,
        'port': 443,
        'use_ssl': True,
        'http_auth': (auth[0], auth[1])
    }]


def get_test_es_config():
    return _get_header("BONSAI_TEST_URL")


def get_production_es_config():
    return _get_header("BONSAI_PRODUCTION_URL")
