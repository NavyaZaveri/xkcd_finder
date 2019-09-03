import os


def test_unauthorized_doc_insertion(server, xkcd_as_json):
    _, response = server.post("/insert", json=xkcd_as_json)
    assert response.status_code == 403
    assert len(server.app.es_client.search_all().results()) == 0


def test_authorized_doc_insertion(server, mock_xkcd):
    _, response = server.post("/insert", json={
        "doc": mock_xkcd.to_dict(),
        "password": os.environ["PASSWORD"]
    })
    server.app.es_client.refresh()
    assert len(server.app.es_client.search_all().results()) == 1
    assert response.status_code == 201


def test_handle_invalid_request(server):
    _, response = server.get("/search", json={
        "wrong_parameter": "foo"
    })
    assert response.status_code == 400


def test_end_to_end_flow(server, mock_xkcd):
    _, response = server.post("/insert", json={
        "doc": mock_xkcd.to_dict(),
        "password": os.environ["PASSWORD"]
    })
    assert response.status_code == 201
    _, response = server.get("/search", params={
        "query": mock_xkcd.content
    })
    assert response.status_code == 200
    assert "results" in response.json
    assert len(response.json["results"]) == 1
    assert response.json["results"][0]["id"] == mock_xkcd.id
