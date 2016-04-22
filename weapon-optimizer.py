import os
import argparse
import json
import copy

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
        # Grab first 10 weapons to start the brute force check
        # Collect the other weapons into a leftover list
        start_list = self.weapon_list[:10]
        leftover_list = self.weapon_list[10:]

        #Calc damage with start_list
        weapon_pool = WeaponPool(start_list)
        best_damage = weapon_pool.calc_damage(summon1, summon2)
        best_pool = weapon_pool

        # Brute Force!
        # Replace each weapon in pool with each leftover weapon
        # If the weapon gets added to the base pool, use that as
        # the basis for the next pass
        current_list = copy.deepcopy(start_list)
        replaced = False
        for leftover_idx in range(len(leftover_list)):
            # Use the best pool as the basis for the next iteration
            if replaced:
                replaced = False
                current_list = copy.deepcopy(best_pool.weapon_list)

            #Replace weapon with leftover weapon one by one to best pool
            for weapon_idx in range(len(current_list)):
                temp_list = copy.deepcopy(current_list)
                temp_list[weapon_idx] = leftover_list[leftover_idx]
                weapon_pool = WeaponPool(temp_list)
                damage = weapon_pool.calc_damage(summon1, summon2)
                if (damage > best_damage):
                    replaced = True
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
