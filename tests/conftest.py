import pytest

from es_api.client import ElasticEngine
from xkcd import Xkcd


@pytest.fixture
def mock_xkcd():
    return Xkcd(
        content="foo"
    )


@pytest.fixture
def client():
    client = ElasticEngine(index="test")
    yield client
    client.destroy_docs_in_current_index(refresh=True)
