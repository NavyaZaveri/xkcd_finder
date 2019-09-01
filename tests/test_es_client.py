import datetime

from es_api.client import ElasticEngine


def test_insertion(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, refresh=True)
    docs = client.search_all().results()
    assert len(docs) == 1


def test_deletion(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, refresh=True)
    client.destroy_docs_in_current_index(refresh=True)
    docs = client.search_all().results()
    assert len(docs) == 0


def test_filter(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd,
                  refresh=True)
    docs = client.search_by(content=mock_xkcd.content).exclude(id=mock_xkcd.id).results()
    assert len(docs) == 0


def test_duplicate_insertions(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, mock_xkcd, refresh=True)
    comics = client.search_all().results()
    assert len(comics) == 1


def test_delete_by(client: ElasticEngine, mock_xkcd):
    client.insert(mock_xkcd, refresh=True)
    assert len([_ for _ in client.search_all().lazy_results()]) == 1

    client.delete_document_by(id=mock_xkcd.id, refresh=True)
    assert len(client.search_all().results()) == 0


def test_size(client: ElasticEngine, new_xkcd_by_content):
    for _ in range(20):
        client.insert(new_xkcd_by_content(), refresh=True)
    assert len(client.search_all().results()) == 20


def test_bulk_indexing(client: ElasticEngine, new_xkcd_by_content):
    actions = (
        {
            "_index": client.index_name,
            "_id": j,
            "_source": new_xkcd_by_content().to_dict()
        }
        for j in range(0, 20)
    )
    client.bulk_insert(actions, refresh=True)
    print(client.search_all().results())
    assert len(client.search_all().results()) == 20


def test_health_check(client: ElasticEngine):
    assert client.ping()
