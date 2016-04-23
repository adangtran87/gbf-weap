from enum import IntEnum

class WeaponSkill(IntEnum):
    none = 0
    small = 1
    medium = 3
    large = 6

class WeaponType(IntEnum):
    normal = 1
    magna = 2
    unknown = 3
    bahamut = 4

class SummonType(IntEnum):
    elemental = 1
    magna = 2
    primal = 3
    ranko = 4
    character = 5

class Weapon(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        output = "{}: {}, {}, {}\n".format(self.name, self.damage, self.weapon_type.name, self.multiplier)
        return output

    @property
    def multiplier(self):
        if self.weapon_skill != WeaponSkill.none:
            return (float(self.weapon_skill) + (self.skill_level - 1)) / 100
        else:
            return float(0)

class Summon(object):
    def __init__(self, type, multiplier):
        if isinstance(type, SummonType):
            self.type = type
            self.multiplier = multiplier
        else:
            raise ValueError("Summon type is not of type SummonType")

