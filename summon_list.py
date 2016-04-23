from wep_types import SummonType, Summon

class SummonList:
    def __init__(self, my_summon, helper_list):
        self.my_summon = my_summon
        self.helper_list = helper_list

    # Pair your summon with each friend list summon
    # @return List of summon pairs
    @property
    def summon_pairs(self):
        summon_pair_list = []
        for helper in self.helper_list:
            summon_pair_list.append((self.my_summon, helper))
        return summon_pair_list
