import hashlib
from abc import ABC, abstractmethod
import attr


class Model(ABC):

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def __eq__(self, other):
        return self.get_id() == other.get_id()


@attr.s(slots=True)
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
