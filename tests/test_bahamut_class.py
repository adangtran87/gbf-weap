import context
import unittest

from weapon import *

class TestBahamutClass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _create_weapon(self, name, damage, weapon_type, skill_level):
        return WeaponBahamut(**{
                                'name':name,
                                'weapon_class':"bahamut",
                                'damage':damage,
                                'weapon_type':weapon_type,
                                'skill_level':skill_level
                                }
                            )

    def _create_hl_weapon(self, name, damage, weapon_type, skill_level):
        return WeaponHLBahamut(**{
                                'name':name,
                                'weapon_class':"hl_bahamut",
                                'damage':damage,
                                'weapon_type':weapon_type,
                                'skill_level':skill_level
                                }
                              )

    def _create_weapon_all(self):
        weapon_list = []
        for index, weapon_type in enumerate(WEAPON_TYPE_LIST):
            weapon = self._create_weapon(str(index), 1000, weapon_type, 1)
            weapon_list.append(weapon)
        return weapon_list

    def _create_hl_weapon_all(self):
        weapon_list = []
        for index, weapon_type in enumerate(WEAPON_TYPE_LIST):
            weapon = self._create_hl_weapon(str(index), 1000, weapon_type, 10)
            weapon_list.append(weapon)
        return weapon_list

    def test_bahamut_skill_limit(self):
        # Expect obejct to be created fine
        success = True
        try:
            weapon=self._create_weapon("1", 1000, "sword", 10)
        except AttributeError:
            success = False

        self.assertTrue(success)

    def test_bahamut_skill_limit_max(self):
        success = False
        try:
            weapon=self._create_weapon("1", 1000, "sword", 11)
        except AttributeError:
            success = True

        self.assertTrue(success)

    def test_hl_bahamut_skill_limit(self):
        success = True
        try:
            weapon=self._create_hl_weapon("1", 1000, "sword", 10)
        except AttributeError:
            success = False

        self.assertTrue(success)

    def test_hl_bahamut_skill_limit_min(self):
        success = False
        try:
            weapon=self._create_hl_weapon("1", 1000, "sword", 9)
        except AttributeError:
            success = True

        self.assertTrue(success)

    # def test_bahamut_human(self):
    #     human_weapons = ['dagger', 'sword']

    #     multiplier_list = []

    #     for weapon in self._create_weapon_all():
    #         if (weapon.multiplier(race=BahamutRace.human) != 0):
    #             multiplier_list.append(weapon)

    #     # Check if correct
    #     for weapon in multiplier_list:
    #         self.assertTrue(weapon.weapon_type in human_weapons)

