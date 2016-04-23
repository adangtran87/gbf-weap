import os
import argparse
import json

from wep_types import WeaponSkill, WeaponType, SummonType, Weapon, Summon
from weapon_list import WeaponList
from summon_list import SummonList

#------------- Optimization Results -----------------------
class OptimizationResults:
    def __init__ (self, damage, pool, summon1, summon2):
        self.damage = damage
        self.pool = pool
        self.my_summon = summon1
        self.helper_summon = summon2

    @property
    def results(self):
        output = ""
        output += "** {} - {} **\n".format(self.my_summon.name, self.helper_summon.name)
        output += "Base Damage: {}\n".format(self.pool.base_damage)
        output += "Damage: {}\n".format(self.damage)
        output += str(self.pool)
        return output

#------------- Parsing ------------------------------------
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
    parser.add_argument('--weapons', '-w', help='Path to weapon json file')
    parser.add_argument('--summons', '-s', help='Path to summon json file')
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

def parse_summon_file(summon_data):
    summon_type_dict = {
        'elemental': SummonType.elemental,
        'magna': SummonType.magna,
        'primal': SummonType.primal,
        'ranko': SummonType.ranko,
        'character': SummonType.character
    }
    summon_data = parse_config_file(summon_data)

    #Parse my summon
    my_summon = summon_data['my_summon']
    my_summon['type'] = summon_type_dict[summon_data['my_summon']['type']]
    my_summon = Summon(**my_summon)

    #Parse helper summons
    helper_summons = []
    for summon_entry in summon_data['helper_list']:
        summon_entry['type'] = summon_type_dict[summon_entry['type']]
        summon = Summon(**summon_entry)
        helper_summons.append(summon)

    return SummonList(my_summon, helper_summons)

#------------- Main ------------------------------------

if __name__ == "__main__":
    args = get_args()

    print ("Parsing: {}".format(args.weapons))
    weapon_list = parse_weapon_file(args.weapons)
    print ("Parsing: {}".format(args.summons))
    summon_list = parse_summon_file(args.summons)

    #Figure out best weapon pool for each summon pair
    result_list = []
    for summon_pair in summon_list.summon_pairs:
        damage, pool = weapon_list.optimize_weapon_summon(summon_pair[0], summon_pair[1])
        result_list.append(OptimizationResults(damage, pool, summon_pair[0], summon_pair[1]))

    # Sort result_list based on damage
    result_list.sort(key=lambda x: x.damage, reverse=True)

    for opt_result in result_list:
        print (opt_result.results)

