import os
import argparse
import json

from weapon import *
from weapon_list import WeaponList
from summon import SummonType, Summon
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

class GranblueWeaponOptimizer(object):
    def __init__(self, weapon_list, summon_list):
        if not (isinstance(weapon_list, WeaponList)):
            raise AttributeError("weapon_list is not a weapon_list")
        if not (isinstance(summon_list, SummonList)):
            raise AttributeError("summon_list is not a SummonList")

        self.weapon_list = weapon_list
        self.summon_list = summon_list

    def optimize(self):
        result_list = []
        self.combination_count = 0
        for summon_pair in self.summon_list.summon_pairs:
            damage, pool, count = self.weapon_list.optimize_weapon_summon(summon_pair[0], summon_pair[1])
            result_list.append(OptimizationResults(damage, pool, summon_pair[0], summon_pair[1]))
            self.combination_count += count

        # Sort result_list based on damage
        result_list.sort(key=lambda x: x.damage, reverse=True)
        return result_list

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
    parser.add_argument('config', metavar='config_file', help='Path to config json file')
    parser.add_argument('--list_all', '-l', dest='list_all', action='store_true', help='Print all optimization results')
    return parser.parse_args()

def parse_weapon_from_data(weapon_data):
    weapon_list = []

    for weapon_entry in weapon_data["weapon_list"]:
        if (weapon_entry['weapon_class'] == "normal"):
            weapon = WeaponNormal(**weapon_entry)
        elif (weapon_entry['weapon_class'] == "normal2"):
            weapon = WeaponNormal2(**weapon_entry['args'])
        elif (weapon_entry['weapon_class'] == "magna"):
            weapon = WeaponMagna(**weapon_entry)
        elif (weapon_entry['weapon_class'] == "unknown"):
            weapon = WeaponUnknown(**weapon_entry)
        elif (weapon_entry['weapon_class'] == "bahamut"):
            weapon = WeaponBahamut(**weapon_entry)
        elif (weapon_entry['weapon_class'] == "hl_bahamut"):
            weapon = WeaponHLBahamut(**weapon_entry)
        elif (weapon_entry['weapon_class'] == "stat_stick"):
            weapon = WeaponStatStick(**weapon_entry)
        weapon_list.append(weapon)

    return WeaponList(weapon_list)

def parse_summon_from_data(summon_data):
    #Parse my summons
    my_summons = []
    for summon_entry in summon_data['my_summons']:
        summon = Summon(**summon_entry)
        my_summons.append(summon)

    #Parse helper summons
    helper_summons = []
    for summon_entry in summon_data['helper_summons']:
        summon = Summon(**summon_entry)
        helper_summons.append(summon)

    return SummonList(my_summons, helper_summons)

#------------- Main ------------------------------------
if __name__ == "__main__":
    args = get_args()

    print ("Parsing: {}".format(args.config))
    config_data = parse_config_file(args.config)
    weapon_list = parse_weapon_from_data(config_data)
    summon_list = parse_summon_from_data(config_data)

    #Figure out best weapon pool for each summon pair
    gwo = GranblueWeaponOptimizer(weapon_list, summon_list)
    result_list = gwo.optimize()
    print ("Parsed {} weapon + summon combinations.\n".format(gwo.combination_count))

    if (args.list_all):
        print_count = len(result_list)
    else:
        print_count = 3

    for opt_result in result_list[:print_count]:
        print (opt_result.results)

