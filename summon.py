from enum import IntEnum
from utils import parse_enum_into_dict

class SummonType(IntEnum):
    elemental = 1
    magna = 2
    primal = 3
    ranko = 4
    character = 5

SUMMON_TYPE_DICT = parse_enum_into_dict(SummonType)

class Summon(object):
    def __init__(self, name, type, multiplier):
        self.name = name
        self.type = SUMMON_TYPE_DICT[type]
        self.multiplier = multiplier

    def __str__(self):
        output = "{}: {}, {}\n".format(self.name, self.type.name, self.multiplier)
        return output

