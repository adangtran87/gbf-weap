import os
import argparse
import json

from weapon import *
from weapon_pool import WeaponPool
from weapon_list import WeaponList
from summon import SummonType, Summon
from summon_list import SummonList
from character import Party, MainCharacter, Character

class GranblueWeaponOptimizer(object):
    def __init__(self, weapon_list, summon_list, party):
        if not (isinstance(weapon_list, WeaponList)):
            raise AttributeError("weapon_list is not a weapon_list")
        if not (isinstance(summon_list, SummonList)):
            raise AttributeError("summon_list is not a SummonList")

        self.weapon_list = weapon_list
        self.summon_list = summon_list
        self.party = party
        self.results = []

    def _find_best_pool_for_summon_pair(self, summon_pair):
        best_damage = 0
        best_pool = None
        count = 0
        character_list = [self.party.mc]
        for party_character in self.party.pc_list:
            character_list.append(party_character)

        # Process all valid pools
        for pool in self.valid_pools:
            count = count+1
            damage = 0

            # Damage aggregates damage from all characters
            for character in character_list:
                damage += pool.calc_damage(summon_pair[0], summon_pair[1], character)

            if (damage > best_damage):
                best_damage = damage
                best_pool = pool

        # Save off best pool and summon pair as tuple
        self.results.append((best_damage, best_pool, summon_pair))
        return count

    def optimize(self):
        self.possible_pools_count = len(self.weapon_list.all_pools)

        self.valid_pools = self.weapon_list.get_valid_pools(party.mc.weapon_preferences)
        self.valid_pools_count = len(self.valid_pools)
        if (self.valid_pools_count == 0):
            raise AttributeError("No weapon pools in WeaponList support Main Character's class.")

        self.execution_count = 0

        for summon_pair in self.summon_list.summon_pairs:
            self.execution_count += self._find_best_pool_for_summon_pair(summon_pair)

        # Sort result_list based on damage
        self.results.sort(key=lambda tup: tup[0], reverse=True)

    def _print_single_result(self, damage, pool, summon_pair):
        output = ""
        output += "** {} - {} **\n".format(summon_pair[0].name, summon_pair[1].name)
        output += "Base Damage: {}\n".format(pool.base_damage)
        output += "Damage: {}\n".format(damage)
        output += str(pool)
        return output

    def print_results(self, list_all):
        print("Weapon Pool Combinations: {}".format(self.possible_pools_count))
        print("Valid Pool Combinations: {}".format(self.valid_pools_count))
        print("Number of pool damage calculations: {}".format(self.execution_count))
        print("")

        # Print characters
        print ("** Party **")
        print (party)

        # Print results
        if (list_all):
            count = 3
        else:
            count = len(self.results)
        for index in range(count):
            damage, pool, summon_pair = self.results[index]
            print(self._print_single_result(damage, pool, summon_pair))

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

def parse_weapon_from_data(parsed_data):
    weapon_list = []

    for weapon_entry in parsed_data["weapon_list"]:
        if (weapon_entry['weapon_class'] == "normal"):
            weapon = WeaponNormal(**weapon_entry)
        elif (weapon_entry['weapon_class'] == "normal2"):
            weapon = WeaponNormal2(**weapon_entry)
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

def parse_summon_from_data(parsed_data):
    #Parse my summons
    my_summons = []
    for summon_entry in parsed_data['my_summons']:
        summon = Summon(**summon_entry)
        my_summons.append(summon)

    #Parse helper summons
    helper_summons = []
    for summon_entry in parsed_data['helper_summons']:
        summon = Summon(**summon_entry)
        helper_summons.append(summon)

    return SummonList(my_summons, helper_summons)

def parse_party_from_data(parsed_data):
    party_data = parsed_data['party']
    mc = MainCharacter(**party_data['main_character'])
    pc_list = []

    if (party_data['party_characters']):
        for party_character in party_data['party_characters']:
            pc_list.append(Character(**party_character))

    return Party(mc, pc_list)

#------------- Main ------------------------------------
if __name__ == "__main__":
    args = get_args()

    print ("Parsing: {}".format(args.config))
    config_data = parse_config_file(args.config)
    weapon_list = parse_weapon_from_data(config_data)
    summon_list = parse_summon_from_data(config_data)
    party = parse_party_from_data(config_data)

    #Figure out best weapon pool for each summon pair
    gwo = GranblueWeaponOptimizer(weapon_list, summon_list, party)
    gwo.optimize()
    gwo.print_results(args.list_all)

