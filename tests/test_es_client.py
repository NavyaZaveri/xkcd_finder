import pytest
from _pytest import unittest

from es_api.client import ElasticEngine


@pytest.fixture
def client():
    client = ElasticEngine(index="test")
    yield client
    client.destroy_documents_in_index("test")


def test_insertion(client):
    pass


def test_deletion(client):
    print("wtf")
    pass
