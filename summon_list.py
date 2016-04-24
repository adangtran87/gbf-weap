from wep_types import SummonType, Summon

class SummonList:
    def __init__(self, my_summons, helper_summons):
        self.my_summons = my_summons
        self.helper_summons = helper_summons

    # Pair your summon with each friend list summon
    # @return List of summon pairs
    @property
    def summon_pairs(self):
        summon_pair_list = []
        for mine in self.my_summons:
            for helper in self.helper_summons:
                summon_pair_list.append((mine, helper))
        return summon_pair_list
