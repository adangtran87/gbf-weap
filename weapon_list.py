import itertools
from wep_types import WeaponType, SummonType, Weapon, Summon
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

    def _sort_weapons(self):
        self.normal_list = []
        self.magna_list = []
        self.unknown_list = []
        self.bahamut_list = []
        self.other_list = []
        #Sort weapons
        for weapon in self.weapon_list:
            if (weapon.weapon_type == WeaponType.normal):
                self.normal_list.append(weapon)
            elif (weapon.weapon_type == WeaponType.magna):
                self.magna_list.append(weapon)
            elif (weapon.weapon_type == WeaponType.unknown):
                self.unknown_list.append(weapon)
            elif (weapon.weapon_type == WeaponType.bahamut):
                self.bahamut_list.append(weapon)
            else:
                self.other_list.append(weapon)

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
