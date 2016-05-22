import itertools
from weapon import *
from summon import SummonType, Summon
from weapon_pool import WeaponPool

class WeaponList:
    def __init__(self, weapon_list):
        self.weapon_list = weapon_list
        return

    def __str__(self):
        output = ""
        output += "Number of weapons: {}\n".format(len(self.weapon_list))
        for weapon in self.weapon_list:
            output += str(weapon)
        return output

    @property
    def all_pools(self):
        return list(itertools.combinations(self.weapon_list, 10))
