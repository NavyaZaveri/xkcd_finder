from es_api.client import ElasticEngine


def test_insertion(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, refresh=True)
    docs = [doc for doc in client.search_all().results()]
    assert len(docs) == 1


def test_deletion(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, refresh=True)
    client.destroy_docs_in_current_index(refresh=True)
    docs = [doc for doc in client.search_all().results()]
    assert len(docs) == 0


def test_filter(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd,
                  refresh=True)
    docs = [d for d in client.search_by(content=mock_xkcd.content).exclude(id=mock_xkcd.id).results()]
    assert len(docs) == 0


def test_duplicate_insertions(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, mock_xkcd, refresh=True)
    comics = [c for c in client.search_all().results()]
    assert len(comics) == 1


def test_delete_by(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, refresh=True)
    assert len([_ for _ in client.search_all().results()]) == 1

    client.delete_document_by(id=mock_xkcd.id, refresh=True)
    assert len([_ for _ in client.search_all().results()]) == 0


def test_health_check(client: ElasticEngine):
    assert client.ping()
