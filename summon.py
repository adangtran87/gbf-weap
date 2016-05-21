from enum import IntEnum

class SummonType(IntEnum):
    elemental = 1
    magna = 2
    primal = 3
    ranko = 4
    character = 5

class Summon(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        output = "{}: {}, {}\n".format(self.name, self.type.name, self.multiplier)
        return output

