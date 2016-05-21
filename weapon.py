from enum import IntEnum
from abc import ABCMeta, abstractmethod, abstractproperty
from utils import parse_enum_into_dict

class WeaponSkill(IntEnum):
    none = 0
    small = 1
    medium = 3
    large = 6

# One hot encoding of race for mask selection
class CharacterRace(IntEnum):
    unknown = 0xF
    human = 1
    erun = 2
    doraf = 4
    harvin = 8

class BahamutType(IntEnum):
    attack= 0
    attack_hp= 1
    hp = 2
    continuous = 3

WEAPON_SKILL_DICT = parse_enum_into_dict(WeaponSkill)

WEAPON_TYPE_LIST = [
        'sword', 'dagger', 'spear', 'axe',
        'staff', 'gun', 'fist', 'bow',
        'harp', 'katana'
    ]

BAHAMUT_MULTIPLIER = {
    BahamutType.attack.name:        [
                                        0.20, 0.21, 0.22, 0.23, 0.24,
                                        0.25, 0.26, 0.27, 0.28, 0.30,
                                    ],
    BahamutType.attack_hp.name:     [
                                        0.10, 0.105, 0.11, 0.115, 0.12,
                                        0.125, 0.13, 0.135, 0.14, 0.15,
                                    ],
    BahamutType.hp.name:            [
                                        0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0,
                                    ],
}

BAHAMUT_TYPE = {
    'sword': BahamutType.attack_hp,
    'dagger': BahamutType.attack,
    'spear': BahamutType.attack,
    'axe': BahamutType.attack,
    'staff': BahamutType.attack_hp,
    'gun': BahamutType.attack,
    'fist': BahamutType.hp,
    'bow': BahamutType.hp,
    'harp': BahamutType.hp,
    'katana': BahamutType.hp,
}

BAHAMUT_RACE = {
    'sword': (CharacterRace.human | CharacterRace.doraf),
    'dagger': CharacterRace.human,
    'spear': CharacterRace.erun,
    'axe': CharacterRace.doraf,
    'staff': (CharacterRace.erun | CharacterRace.harvin),
    'gun': CharacterRace.harvin,
    'fist': CharacterRace.human,
    'bow': CharacterRace.erun,
    'harp': CharacterRace.harvin,
    'katana': CharacterRace.doraf,
}

HL_BAHAMUT_MULTIPLIER = {
    BahamutType.attack_hp.name:     [
                                        0.300, 0.304, 0.308,
                                        0.312, 0.316, 0.320
                                    ],
    BahamutType.continuous.name:    [
                                        0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0,
                                    ],
}

HL_BAHAMUT_TYPE = {
    'sword': BahamutType.attack_hp,
    'dagger': BahamutType.attack_hp,
    'spear': BahamutType.attack_hp,
    'axe': BahamutType.attack_hp,
    'staff': BahamutType.attack_hp,
    'gun': BahamutType.attack_hp,
    'fist': BahamutType.continuous,
    'bow': BahamutType.continuous,
    'harp': BahamutType.continuous,
    'katana': BahamutType.continuous,
}

HL_BAHAMUT_RACE= {
    'sword': (CharacterRace.human | CharacterRace.doraf),
    'dagger': (CharacterRace.human | CharacterRace.erun),
    'spear': (CharacterRace.erun | CharacterRace.doraf),
    'axe': (CharacterRace.doraf | CharacterRace.harvin),
    'staff': (CharacterRace.erun | CharacterRace.harvin),
    'gun': (CharacterRace.harvin | CharacterRace.human),
    'fist': CharacterRace.human,
    'bow': CharacterRace.erun,
    'harp': CharacterRace.harvin,
    'katana': CharacterRace.doraf,
}

###############################################################################
# Weapon Abstract Class
###############################################################################
class WeaponBase(object):
    __metaclass__ = ABCMeta

    def __str__(self):
        output = "{}: {}, {}, {}\n".format(self.name, self.damage, self.weapon_class, self.multiplier)
        return output

    @abstractproperty
    def multiplier(self):
        """Return the multiplier of that weapon."""
        raise NotImplementedError()

###############################################################################
# Weapon Types
###############################################################################

class WeaponStatStick(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.skill_level = 0
        return

    @property
    def multiplier(self):
        return 0

class WeaponNormal(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.weapon_skill = WEAPON_SKILL_DICT[self.weapon_skill]
        return

    @property
    def multiplier(self):
        return (float(self.weapon_skill) + (self.skill_level - 1)) / 100

class WeaponNormal2(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.weapon_skill = WEAPON_SKILL_DICT[self.weapon_skill]
        return

    @property
    def multiplier(self):
        return (float(self.weapon_skill) + (self.skill_level - 1) + 1) / 100

class WeaponMagna(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.weapon_skill = WEAPON_SKILL_DICT[self.weapon_skill]
        return

    @property
    def multiplier(self):
        return (float(self.weapon_skill) + (self.skill_level - 1)) / 100

class WeaponUnknown(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.weapon_skill = WEAPON_SKILL_DICT[self.weapon_skill]
        return

    @property
    def multiplier(self):
        return (float(self.weapon_skill) + (self.skill_level - 1)) / 100

class WeaponStrength(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.weapon_skill = WEAPON_SKILL_DICT[self.weapon_skill]
        return

    @property
    def multiplier(self):
        return (float(self.weapon_skill) + (self.skill_level - 1)) / 100

class WeaponBahamut(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        if self.skill_level > 10:
            raise AttributeError("Bahamut weapon skill levels cannot be above 10. Use HL Bahamut class.")

        self.bahamut_type = BAHAMUT_TYPE[self.weapon_type]
        self.bahamut_race = BAHAMUT_RACE[self.weapon_type]
        self.applied_race = CharacterRace.unknown
        return

    @property
    def multiplier(self):
        multiplier = 0
        # If matching one of the race flags
        if (self.applied_race & self.bahamut_race != 0):
            multiplier = BAHAMUT_MULTIPLIER[self.bahamut_type.name][self.skill_level-1]
        else:
            multiplier = 0

        return multiplier

class WeaponHLBahamut(WeaponBase):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        if self.skill_level < 10:
            raise AttributeError("HL Bahamut weapons cannot be less than 10. Use Bahamut class")

        self.bahamut_type = HL_BAHAMUT_TYPE[self.weapon_type]
        self.bahamut_race = HL_BAHAMUT_RACE[self.weapon_type]
        self.applied_race = CharacterRace.unknown
        return

    @property
    def multiplier(self):
        multiplier = 0
        # If matching one of the race flags
        if (self.applied_race & self.bahamut_race != 0):
            multiplier = HL_BAHAMUT_MULTIPLIER[self.bahamut_type.name][self.skill_level-10]
        else:
            multiplier = 0

        return multiplier

