from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index

from xkcd import Xkcd

'''
e = Elasticsearch()

e.index("wtf", {"beansie": "bneabie"})
q = {"x": "3"}
a = Xkcd(10, "python good")
b = Xkcd(20, "better python")
c = Xkcd(20, "best")
e.index("wtf", a.to_dict())
e.index("wtf", b.to_dict())
e.index("wtf", c.to_dict())
s: Search = Search(using=e, index="wtf").query("match", content="good python")
ind = Index("wtf", using=e)
for i in s:
    print(i.to_dict())
res = Search(using=e, index="wtf").query("match_all").delete()
print(res)
'''


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
        :type docs: Model
        """
        refresh = kwargs.pop("refresh", False)
        for doc in docs:
            if hasattr(doc, "to_dict"):
                json = doc.to_dict()
            else:
                json = doc

            self._client.index(self.index_name, json)
            if refresh:
                self.refresh()

    def results(self):
        for match in self._search.execute():
            yield match.to_dict()

        # reset
        self._search = Search(using=self._client, index=self.index_name)
