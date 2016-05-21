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

    def optimize_weapon_summon(self, summon1, summon2):
        best_damage = 0
        best_pool = None
        count = 0

        #Brute force all combinations!
        for weap_comb in itertools.combinations(self.weapon_list, 10):
            weapon_pool = WeaponPool(weap_comb)
            damage = weapon_pool.calc_damage(summon1, summon2)
            count += 1
            if (damage > best_damage):
                best_damage = damage
                best_pool = weapon_pool

        return best_damage, best_pool, count
