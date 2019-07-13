import time

import elasticsearch_dsl
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index

e = Elasticsearch()

e.index("wtf", {"hello": "world"})
q = {"hello": "coopsie"}
for i in range(3):
    e.index("wtf", q)
s: Search = Search(using=e, index="wtf").query("match_all").exclude("match", hello="world")
i = Index("wtf", using=e)
i.refresh()
for i in s:
    print(i.to_dict())

res = Search(using=e, index="wtf").query("match_all").delete()
print(res)


def sigh(**kwargs):
    print(kwargs)


def thing(**kwargs):
    sigh(**kwargs)


class ElasticEngine:
    def __init__(self, index):
        self._client = Elasticsearch()
        self._search = Search(using=self._client, index=index)

    def _refres(self):

    def search_all(self, index):
        self._search = self._search.query("match_all")

    def destroy_index(self, index):
        self._search.index(index).delete()

    def destroy_documents_in_index(self, index):
        self._search.query("match_all").delete()

    def search_by(self, fuzzy, **kwargs):
        self._search = self._search.query("fuzzy", **kwargs)
        return self

    def exclude(self, **kwargs):
        self._search = self._search.exclude("match", **kwargs)

    def get(self):
        for match in self._search.execute():
            yield match.to_dict()
