import pytest
from es_api.client import ElasticEngine


@pytest.fixture()
def client():
    e = ElasticEngine("test_index")
    yield e
    e.destroy_index("test_index")
