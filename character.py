from enum import IntEnum
from utils import parse_enum_into_dict

# One hot encoding of race for mask selection
class CharacterRace(IntEnum):
    unknown = 0xF
    human = 1
    erun = 2
    doraf = 4
    harvin = 8

CLASS_WEAPON_PREF = {
    # Tier 3
    'weapon_master': ['sword','axe'],
    'holy_saber': ['sword', 'spear'],
    'bishop': ['staff', 'spear'],
    'hermit': ['staff', 'dagger'],
    'hawkeye': ['dagger', 'gun'],
    'dark_fencer': ['sword', 'dagger'],
    'ogre': ['fist'],
    'sidewinder': ['bow', 'gun'],
    'superstar': ['harp', 'dagger'],
    'valkyrie': ['spear', 'axe'],
    # Tier 4
    'berserker': ['sword', 'axe'],
    'sage': ['staff', 'spear'],
    # Extra
    'alchemist': ['dagger', 'gun'],
    'ninja': ['katana', 'fist'],
    'samurai': ['katana', 'bow'],
    'sword_master': ['sword', 'katana'],
    'gunslinger': ['gun'],
    'mystic': ['staff'],
    'assassin': ['dagger'],
}

CHARACTER_RACE_DICT = parse_enum_into_dict(CharacterRace)

class Character(object):
    def __init__(self, name, wep_pref, race):
        self.name = name
        self.weapon_preferences = str(wep_pref)
        self.race = CHARACTER_RACE_DICT[race]

    def __str__(self):
        output = ""
        output += "{}, {}, {}\n".format(self.name, self.race.name, self.weapon_preferences)
        return output

class MainCharacter(Character):
    def __init__(self, name, char_class, race):
        Character.__init__(self, name, CLASS_WEAPON_PREF[char_class], race)

class Party(object):
    def __init__(self, mc, pc_list):
        if not (isinstance(mc, MainCharacter)):
            raise AttributeError("main character class is not MainCharacter class.")
        self.mc = mc
        self.pc_list = pc_list

    def __str__(self):
        output = ""
        output += str(self.mc)
        for pc in self.pc_list:
            output += str(pc)
        return output
