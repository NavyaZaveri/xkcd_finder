import pytest

from es_api.client import ElasticEngine
from models.xkcd import Xkcd


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
