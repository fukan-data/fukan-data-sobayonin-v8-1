from enum import Enum


class BaseEnum(Enum):
    def __init__(self, no, ja, en):
        self.no = no
        self.ja = ja
        self.en = en

    @classmethod
    def choices(cls):
        return [(member.no, member.ja) for member in cls]
