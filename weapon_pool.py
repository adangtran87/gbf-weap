from wep_types import WeaponType, SummonType, Weapon, Summon

class WeaponPool(object):
    def __new__(cls, weapon_pool):
        if (len(weapon_pool) > 10):
            # Cannot create a weapon pool object with greater than 10 weapons
            raise ValueError("Weapon pool cannot be larger than 10 weapons")
        else:
            return super(WeaponPool, cls).__new__(cls)

    # Initialize with a list of 10 weapons
    def __init__(self, weapon_pool):
        self.weapon_list= weapon_pool

        self.normal_list = []
        self.magna_list = []
        self.unknown_list = []
        self.bahamut_list = []
        self.other_list = []

        self.base_damage = 0

        # Sort weapons
        for weapon in weapon_pool:
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

            self.base_damage += weapon.damage

        self.normal_modifier = self._calc_multiplier(self.normal_list)
        self.magna_modifier = self._calc_multiplier(self.magna_list)
        self.unknown_modifier = self._calc_multiplier(self.unknown_list)
        self.bahamut_modifier = self._calc_multiplier(self.bahamut_list)

    def __str__(self):
        output = ""
        output += "Number of weapons: {}\n".format(len(self.weapon_list))
        for weapon in self.weapon_list:
            output += str(weapon)
        output += "N:{} M:{} U:{} B:{}\n".format(self.normal_modifier, self.magna_modifier, self.unknown_modifier, self.bahamut_modifier)
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
        summon_mult['elemental'] = 1
        for summon in summon_list:
            if (summon.type == SummonType.magna):
                summon_mult['magna'] += summon.multiplier
            elif (summon.type == SummonType.primal):
                summon_mult['primal'] += summon.multiplier
            elif (summon.type == SummonType.ranko):
                summon_mult['ranko'] += summon.multiplier
            elif (summon.type == SummonType.elemental):
                summon_mult['elemental'] += summon.multiplier

        return summon_mult

    def calc_damage(self, my_summon, friend_summon):
        # Calc summon multipliers
        summon_mult = self._calc_summon_multipliers([my_summon, friend_summon])

        # Calculate each modifier
        magna_mod = 1 + (self.magna_modifier * summon_mult['magna'])

        normal_mod = 1 + (self.normal_modifier * summon_mult['primal'])
        normal_mod += self.bahamut_modifier

        unknown_mod = 1 + (self.unknown_modifier * summon_mult['ranko'])

        elemental_mod = summon_mult['elemental']

        #Calculate total damage
        damage = 0
        damage = self.base_damage * magna_mod * normal_mod * unknown_mod * elemental_mod
        return round(damage, 2)

