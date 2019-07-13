import time

import elasticsearch_dsl
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index

e = Elasticsearch()

e.index("wtf", {"beansie": "bneabie"})
q = {"caputtt": "coopsie"}
for i in range(3):
    e.index("wtf", q)
s: Search = Search(using=e, index="wtf").query("match_all").exclude("match", hello="world")

ind = Index("wtf", using=e)
ind.refresh()

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
        self.index_name = index
        self._client = Elasticsearch()
        self._search = Search(using=self._client, index=index)
        self._index = Index(name=index, using=self._client)

    def refresh(self):
        self._index.refresh()

    def search_all(self):
        self._search = self._search.query("match_all")

    def destroy_index(self, index):
        self._search.index(index).delete()
        self._index.refresh()

    def destroy_documents_in_index(self, index):
        self._search.query("match_all").delete()
        self.refresh()

    def search_by(self, search_type="fuzzy", **kwargs):
        self._search = self._search.query(search_type, **kwargs)
        return self

    def exclude(self, **kwargs):
        self._search = self._search.exclude("match", **kwargs)

    def insert(self, doc):
        self._client.index(self.index_name, doc)
        self.refresh()

    def get(self):
        for match in self._search.execute():
            yield match.to_dict()
