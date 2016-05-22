from weapon import *
from summon import SummonType, Summon

class WeaponPool(object):
    def __new__(cls, weapon_pool):
        if (len(weapon_pool) > 10):
            # Cannot create a weapon pool object with greater than 10 weapons
            raise ValueError("Weapon pool cannot be larger than 10 weapons")
        else:
            return super(WeaponPool, cls).__new__(cls)

    # Initialize with a list of 10 weapons
    def __init__(self, weapon_pool):
        self.weapon_pool= weapon_pool

        self.normal_list = []
        self.magna_list = []
        self.unknown_list = []
        self.bahamut_list = []
        self.strength_list = []
        self.other_list = []

        # Sort weapons
        for weapon in weapon_pool:
            if (isinstance(weapon, WeaponNormal) or isinstance(weapon,WeaponNormal2)):
                self.normal_list.append(weapon)
            elif (isinstance(weapon, WeaponMagna)):
                self.magna_list.append(weapon)
            elif (isinstance(weapon, WeaponUnknown)):
                self.unknown_list.append(weapon)
            elif (isinstance(weapon, WeaponStrength)):
                self.strength_list.append(weapon)
            elif (isinstance(weapon, WeaponBahamut) or isinstance(weapon, WeaponHLBahamut)):
                self.bahamut_list.append(weapon)
            else:
                self.other_list.append(weapon)

        self.normal_modifier = round(self._calc_multiplier(self.normal_list),2)
        self.magna_modifier = round(self._calc_multiplier(self.magna_list),2)
        self.unknown_modifier = round(self._calc_multiplier(self.unknown_list),2)
        self.strength_modifier = round(self._calc_multiplier(self.strength_list),2)

        """ Section 3.7
        For stacking rules, there is a limit on damage increase from bahamut
        weapons (50%), you can stack two HL Bahamut weapons to give a mono race
        maximum bonus of 50% Damage and 36% Health. You can also stack a HL
        Bahamut Weapon with another Bahamut Weapon.
        """
        self.bahamut_modifier = round(self._calc_multiplier(self.bahamut_list),2)
        if self.bahamut_modifier > 0.5:
            self.bahamut_modifier = 0.5

    def __str__(self):
        output = ""
        output += "Number of weapons: {}\n".format(len(self.weapon_pool))
        for weapon in self.weapon_pool:
            output += str(weapon)
        output += "N:{:.2f} M:{:.2f} U:{:.2f} S:{:.2f} B:{:.2f}\n".format(
                   self.normal_modifier,
                   self.magna_modifier,
                   self.unknown_modifier,
                   self.strength_modifier,
                   self.bahamut_modifier)
        return output

    @property
    def normal_count(self):
        return len(normal_list)
    @property
    def magna_count(self):
        return len(magna_count)
    @property
    def unknown_count(self):
        return len(unknown_list)
    @property
    def bahamut_count(self):
        return len(bahamut_list)

    def _calc_multiplier(self, weapon_list):
        multiplier = 0
        for weapon in weapon_list:
            multiplier += weapon.multiplier
        return multiplier

    def _calc_summon_multipliers(self, summon_list):
        summon_mult = {}
        # Figure out summon multipliers
        summon_mult['magna'] = 1
        summon_mult['primal'] = 1
        summon_mult['ranko'] = 1
        summon_mult['elemental'] = 0
        summon_mult['character'] = 0
        for summon in summon_list:
            if (summon.type == SummonType.magna):
                summon_mult['magna'] += summon.multiplier
            elif (summon.type == SummonType.primal):
                summon_mult['primal'] += summon.multiplier
            elif (summon.type == SummonType.ranko):
                summon_mult['ranko'] += summon.multiplier
            elif (summon.type == SummonType.elemental):
                summon_mult['elemental'] += summon.multiplier
            elif (summon.type == SummonType.character):
                summon_mult['character'] += summon.multiplier

        return summon_mult

    def calc_base_damage(self, weapon_preferences=[]):
        total_damage = 0
        for weapon in self.weapon_pool:
            total_damage += weapon.damage
        return total_damage

    #return unmodified base damage
    @property
    def base_damage(self):
        return self.calc_base_damage()

    def calc_damage(self, my_summon, friend_summon, wep_pref=[]):
        base_damage = self.calc_base_damage(wep_pref)
        # Calc summon multipliers
        summon_mult = self._calc_summon_multipliers([my_summon, friend_summon])

        # Calculate each modifier
        magna_mod = 1 + (self.magna_modifier * summon_mult['magna'])

        normal_mod = 1 + (self.normal_modifier * summon_mult['primal'])
        normal_mod += self.bahamut_modifier
        normal_mod += summon_mult['character']

        unknown_mod = 1 + (self.unknown_modifier * summon_mult['ranko'])
        unknown_mod += self.strength_modifier

        elemental_mod = 1 + summon_mult['elemental']

        #Calculate total damage
        damage = 0
        damage = base_damage * magna_mod * normal_mod * unknown_mod * elemental_mod
        return round(damage, 2)

