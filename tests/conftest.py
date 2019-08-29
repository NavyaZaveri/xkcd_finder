import json

import pytest

from es_api.client import ElasticEngine
from models.xkcd import Xkcd
from server.app import app
from scraper.async_scheduler import AsyncRequestScheduler


@pytest.fixture
def mock_xkcd():
    return Xkcd(
        content="foo",
        link="https://foo.com",
        title="bar"
    )


@pytest.fixture
def client():
    client = ElasticEngine.from_bonsai("test", test_instance=True)
    yield client
    client.delete_index("test")


@pytest.fixture
def server(client):
    @app.listener('before_server_start')
    async def setup_db(app, loop):
        app.es_client = client

    yield app.test_client


@pytest.fixture
def xkcd_as_json(mock_xkcd):
    return json.dumps(mock_xkcd.to_dict())


@pytest.fixture
def new_xkcd_by_content():
    content = 1

    def inner():
        nonlocal content
        content += 1
        return Xkcd(
            content=str(content),
            link="http://foobarr.com",
            title="bar"
        )

    return inner


@pytest.fixture
def async_scraper():
    return AsyncRequestScheduler(wait=2)


@pytest.fixture
def google_get():
    async def inner():
        pass
