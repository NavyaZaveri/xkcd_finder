import pytest

from es_api.client import ElasticEngine
from xkcd import Xkcd


@pytest.fixture
def client():
    client = ElasticEngine(index="test")
    yield client
    client.destroy_docs_in_current_index(refresh=True)


def test_insertion(client):
    """
    :type client: ElasticEngine
    """
    client.insert(Xkcd("b", "c"), refresh=True)
    client.insert(Xkcd("y", "z"), refresh=True)
    docs = [doc for doc in client.search_all().results()]
    assert len(docs) == 2


def test_deletion(client):
    """
    :type client: ElasticEngine
    """
    client.insert(Xkcd("key1", "thing1"), Xkcd("key2", "thing2"), refresh=True)
    client.destroy_docs_in_current_index(refresh=True)
    docs = [doc for doc in client.search_all().results()]
    assert len(docs) == 0


def test_filter(client):
    """
    :type client: ElasticEngine
    """
    client.insert(Xkcd("thing", "xyz", id=100),
                  Xkcd("thing", "abc", id=200),
                  refresh=True)
    docs = [d for d in client.search_by(content="thing").exclude(id=100).results()]
    assert len(docs) == 1


def test_multiple_queries(client):
    """

    :type client: ElasticEngine
    """
    client.insert(Xkcd("name", "thing", id=100),
                  Xkcd("name", "thing", id=200),
                  refresh=True)
    _ = [_ for _ in client.search_by(link="thing").results()]
    client.insert(Xkcd("new_name", "new_thing", id=50),
                  refresh=True)
    docs = [_ for _ in client.search_by(link="new_thing").results()]
    assert len(docs) == 1


def test_update(client):
    """

    :type client: ElasticEngine
    """
    old = Xkcd("a", "b", id=100)
    updated = Xkcd("c", "d", id=100)

    client.insert(old, refresh=True)
    client.update(old, updated, refresh=True)
    docs = [i for i in client.search_by(id=100).results()]
    assert len(docs) == 1
    assert docs[0]["content"] == "c"

    client.delete_document(updated, refresh=True)
    docs = [i for i in client.search_by(id=100).results()]
    assert len(docs) == 0


def test_duplicate_insertions(client: ElasticEngine):
    a = Xkcd(content="hello")
    b = Xkcd(content="hello")
    client.insert(a, b, refresh=True)
    comics = [c for c in client.search_all().results()]
    assert len(comics) == 1
