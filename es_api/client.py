from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index
from abc import ABC, abstractmethod

e = Elasticsearch()


class Model(ABC):

    def to_dict(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    def __eq__(self, other):
        return self.id == other.id


class Xkcd(Model):
    def __init__(self, id, content, link):
        self.id = id
        self.content = content
        self.link = link

    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "link": self.link
        }


e.index("wtf", {"beansie": "bneabie"})
q = {"x": "3"}
for i in range(3):
    e.index("wtf", q)
    s: Search = Search(using=e, index="wtf").query("match", x=3).exclude("match", hello="world")

ind = Index("wtf", using=e)
ind.refresh()

for i in s:
    print(i.to_dict())

res = Search(using=e, index="wtf").query("match_all").delete()
print(res)

c = Xkcd("a", "v", "c")


class ElasticEngine:
    def __init__(self, index):
        self.index_name = index
        self._client = Elasticsearch()
        self._search = Search(using=self._client, index=index)
        self._index = Index(name=index, using=self._client)

    def refresh(self):
        self._index.refresh()

    def update(self, old, new_doc, refresh=False):
        """

        :param new_doc: Model
        :param refresh:
        :type old: Model
        """
        docs = [d for d in self.search_by(id=old.get_id()).results()]
        if len(docs) > 1:
            raise ValueError("shite")
        if not docs:
            raise ValueError("no such document ")
        self.delete_document(old, refresh=refresh)
        self.insert(new_doc, refresh=refresh)

    def search_all(self):
        self._search = self._search.query("match_all")
        return self

    def destroy_index(self, index, refresh=False):
        self._search.index(index).delete()
        if refresh:
            self.refresh()

    def delete_document(self, doc, **kwargs):
        self._search.query("match", id=doc.get_id()).delete()
        refresh = kwargs.pop("refresh", False)
        if refresh:
            self.refresh()

    def destroy_docs_in_current_index(self, refresh=False):

        self._search.query("match_all").delete()
        if refresh:
            self.refresh()

    def search_by(self, search_type="match", **kwargs):
        self._search = self._search.query(search_type, **kwargs)
        return self

    def exclude(self, **kwargs):
        self._search = self._search.exclude("match", **kwargs)
        return self

    def insert(self, *docs, **kwargs):
        """
        :param refresh:
        :type docs: Model
        """
        refresh = kwargs.pop("refresh", False)
        for doc in docs:
            self._client.index(self.index_name, doc.to_dict())
            if refresh:
                self.refresh()

    def results(self):
        for match in self._search.execute():
            yield match.to_dict()

        # reset
        self._search = Search(using=self._client, index=self.index_name)
