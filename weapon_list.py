import itertools
from weapon import *
from summon import SummonType, Summon
from weapon_pool import WeaponPool

class WeaponList:
    def __init__(self, weapon_list):
        self.weapon_list = weapon_list
        self.all_pools = []
        for pool in (itertools.combinations(self.weapon_list, 10)):
            pool = WeaponPool(pool)
            self.all_pools.append(pool)
        return

    def __str__(self):
        output = ""
        output += "Number of weapons: {}\n".format(len(self.weapon_list))
        for weapon in self.weapon_list:
            output += str(weapon)
        return output

    def get_valid_pools(self, required_weapons):
        valid_pools = []
        for pool in self.all_pools:
            if pool.isValid(required_weapons):
                valid_pools.append(pool)
        return valid_pools
