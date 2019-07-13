import pytest
from _pytest import unittest

from es_api.client import ElasticEngine


@pytest.fixture
def client():
    yield ElasticEngine(index="test")


def test_insertion(client):
    c = client
    print(c.__dict__)


def test_deletion(client):
    print("wtf")
    pass
