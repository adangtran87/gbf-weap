import os
import argparse
import json
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

    def optimize_weapons(self):
        #self._sort_weapons()
        elemental_50 = Summon(SummonType.elemental, .5)
        elemental_60 = Summon(SummonType.elemental, .6)
        magna_50 = Summon(SummonType.magna, .5)
        magna_100 = Summon(SummonType.magna, 1)

        # Get the first 10 weapons as a weapon pool
        weapon_pool = WeaponPool(self.weapon_list[0:10])

        #Calc damage with different summons
        ele50_ele60 = weapon_pool.calc_damage(elemental_50, elemental_60)
        ele50_magna50 = weapon_pool.calc_damage(elemental_50, magna_50)
        ele50_magna100 = weapon_pool.calc_damage(elemental_50, magna_100)

        print (weapon_pool)
        print ("Base Damage = {}".format(weapon_pool.base_damage))
        print ("Elemental 50% + Elemental 60% = {}".format(ele50_ele60))
        print ("Elemental 50% + Magna 50% = {}".format(ele50_magna50))
        print ("Elemental 50% + Magna 100% = {}".format(ele50_magna100))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help='Path to weapon json file')
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    print args.config

    weapon_list = WeaponList(args.config)
    weapon_list.optimize_weapons()
