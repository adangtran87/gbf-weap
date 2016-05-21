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

class Weapon(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        output = "{}: {}, {}, {}\n".format(self.name, self.damage, self.weapon_type.name, self.multiplier)
        return output

    @property
    def multiplier(self):
        bahamut_multiplier = [
            0.20, 0.21, 0.22, 0.23, 0.24,
            0.25, 0.26, 0.27, 0.28, 0.30,
            0.304, 0.308, 0.312, 0.316, 0.320,
        ]
        if self.weapon_type == WeaponType.bahamut:
            return bahamut_multiplier[self.skill_level - 1]
        else:
            if self.weapon_skill != WeaponSkill.none:
                return (float(self.weapon_skill) + (self.skill_level - 1)) / 100
            else:
                return float(0)

