import os
import argparse
import json
import copy
import itertools

from wep_types import WeaponType, SummonType, Weapon, Summon
from weapon_pool import WeaponPool

class WeaponList:
    def __new__(cls, weapon_file):
        root, ext = os.path.splitext(weapon_file)
        if ext in file_parsers.keys():
            return super(Test, cls).__new__(cls)
        else:
            raise ValueError("Cannot parse file of {} extension".format(ext))

    def __init__(self, weapon_file):
        self.file_parsers = {
            '.json': self._parse_json,
        }

        self.weapon_list = []
        root, ext = os.path.splitext(weapon_file)
        self.weapon_list = self.file_parsers[ext](weapon_file)
        return

    def __str__(self):
        output = ""
        output += "Number of weapons: {}\n".format(len(self.weapon_list))
        for weapon in self.weapon_list:
            output += str(weapon)
        return output

    def _parse_json(self, weapon_file):
        weapon_list = []
        with open(weapon_file) as json_data:
            weapon_data = json.load(json_data)

        for weapon_entry in weapon_data["weapon_list"]:
            weapon = Weapon(**weapon_entry)
            weapon_list.append(weapon)
        return weapon_list

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

        #Brute force all combinations!
        for weap_comb in itertools.combinations(self.weapon_list, 10):
            weapon_pool = WeaponPool(weap_comb)
            damage = weapon_pool.calc_damage(summon1, summon2)
            if (damage > best_damage):
                best_damage = damage
                best_pool = weapon_pool

        return best_damage, best_pool

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help='Path to weapon json file')
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    print ("Parsing: {}".format(args.config))

    weapon_list = WeaponList(args.config)

    # Create summons I care about right now
    # Need to figure out best way to let users specify which combinations they care about
    elemental_50 = Summon(SummonType.elemental, .5)
    elemental_60 = Summon(SummonType.elemental, .6)
    magna_50 = Summon(SummonType.magna, .5)
    magna_100 = Summon(SummonType.magna, 1)

    # Print results!
    print ("** Elemental 50 - Elemental 60 **")
    damage, pool = weapon_list.optimize_weapon_summon(elemental_50, elemental_60)
    print ("Base Damage: {}".format(pool.base_damage))
    print ("Damage: {}".format(damage))
    print (pool)

    print ("** Elemental 50 - Magna 50 **")
    damage, pool = weapon_list.optimize_weapon_summon(elemental_50, magna_50)
    print ("Base Damage: {}".format(pool.base_damage))
    print ("Damage: {}".format(damage))
    print (pool)

    print ("** Elemental 50 - Magna 100 **")
    damage, pool = weapon_list.optimize_weapon_summon(elemental_50, magna_100)
    print ("Base Damage: {}".format(pool.base_damage))
    print ("Damage: {}".format(damage))
    print (pool)
