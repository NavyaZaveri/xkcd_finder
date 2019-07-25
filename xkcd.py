import attr

from es_api.client import Model


@attr.s
class Xkcd(Model):
    def to_dict(self):
        return attr.asdict(self)

    def get_id(self):
        return self.id

    id = attr.ib()
    content = attr.ib(default="")
    link = attr.ib(default="")
    title = attr.ib(default="")
    neighbors = attr.ib(default=[])
