import hashlib
from abc import ABC, abstractmethod
import attr

import utils


class Model(ABC):

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def __eq__(self, other):
        return self.get_id() == other.get_id()


@attr.s(slots=True, frozen=True)
class Xkcd(Model):
    content = attr.ib()
    link = attr.ib()
    title = attr.ib()
    id = attr.ib()

    @id.default
    def make_id(self):
        return int(hashlib.sha256(self.content.encode('utf-8')).hexdigest(), 16) % 10 ** 8

    def get_id(self):
        return self.id

    def to_dict(self):
        return attr.asdict(self)

    @classmethod
    def from_json(cls, xkcd_json):
        xkcd_json["transcript"] = utils.cleanup(xkcd_json["transcript"])
        return cls(
            content=xkcd_json["transcript"],
            title=xkcd_json["title"],
            link=xkcd_json["img"],
        )
