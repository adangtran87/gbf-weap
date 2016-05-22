from enum import IntEnum

# One hot encoding of race for mask selection
class CharacterRace(IntEnum):
    unknown = 0xF
    human = 1
    erun = 2
    doraf = 4
    harvin = 8

# class Character(object):
#     def __init__(self, name, wep_pref, race):
#         self.name = name
#         self.weapon_preferences = wep_pref
#         self.race = race
