import pytest

from es_api.client import ElasticEngine


@pytest.fixture
def client():
    client = ElasticEngine(index="test")
    yield client
    client.destroy_docs_in_current_index(refresh=True)


def test_insertion(client):
    client.insert({"hell0": "world"}, refresh=True)
    client.insert({"foo": "bar"}, refresh=True)
    docs = [doc for doc in client.search_all().get()]
    print(docs)
    assert len(docs) == 2


def test_deletion(client):
    client.insert({"key1": "thing1"}, {"key2": "thing2"}, refresh=True)
    client.destroy_docs_in_current_index(refresh=True)
    docs = [doc for doc in client.search_all().get()]
    assert len(docs) == 0
