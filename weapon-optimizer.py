import os
import argparse
import json

from wep_types import WeaponSkill, WeaponType, SummonType, Weapon, Summon
from weapon_list import WeaponList

def parse_config_file(file_data):
    root, ext = os.path.splitext(file_data)
    return FILE_PARSERS[ext](file_data)

def parse_json(file_data):
    with open(file_data) as json_data:
        data_dict = json.load(json_data)
    return data_dict

FILE_PARSERS = {
    '.json': parse_json,
}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weapon', '-w', help='Path to weapon json file')
    return parser.parse_args()

def parse_weapon_file(weapon_data):
    weapon_type_dict= {
        'normal': WeaponType.normal,
        'magna': WeaponType.magna,
        'unknown': WeaponType.unknown,
        'bahamut': WeaponType.bahamut,
    }
    weapon_skill_dict = {
        'none': WeaponSkill.none,
        'small': WeaponSkill.small,
        'medium': WeaponSkill.medium,
        'large': WeaponSkill.large,
    }
    weapon_list = []
    weapon_data = parse_config_file(weapon_data)

    for weapon_entry in weapon_data["weapon_list"]:
        # Replace strings with types
        weapon_entry['weapon_type'] = weapon_type_dict[weapon_entry['weapon_type']]
        weapon_entry['weapon_skill'] = weapon_skill_dict[weapon_entry['weapon_skill']]
        weapon = Weapon(**weapon_entry)
        weapon_list.append(weapon)

    return WeaponList(weapon_list)

if __name__ == "__main__":
    args = get_args()

    print ("Parsing: {}".format(args.weapon))
    weapon_list = parse_weapon_file(args.weapon)

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
