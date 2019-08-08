import os
import re

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path,verbose=True)


def _get_header(url):
    bonsai_url = os.environ[url]
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
