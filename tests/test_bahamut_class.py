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

    def _find_bahamut_weapon_appiled_race(self, weapon_list, race):
        multiplier_list = []
        for weapon in weapon_list:
            weapon.applied_race = race
            if (weapon.multiplier != 0):
                multiplier_list.append(weapon)

        return multiplier_list

    def test_bahamut_human(self):
        reg_pass = ['dagger', 'sword']
        hl_pass = ['dagger', 'gun', 'sword']

        reg_list = self._create_weapon_all()
        reg_list = self._find_bahamut_weapon_appiled_race(reg_list, CharacterRace.human)

        hl_list = self._create_hl_weapon_all()
        hl_list = self._find_bahamut_weapon_appiled_race(hl_list, CharacterRace.human)

        for weapon in reg_list:
            self.assertTrue(weapon.weapon_type in reg_pass)

        for weapon in hl_list:
            self.assertTrue(weapon.weapon_type in hl_pass)

    def test_bahamut_doraf(self):
        reg_pass = ['axe', 'sword']
        hl_pass = ['axe', 'spear', 'sword']

        reg_list = self._create_weapon_all()
        reg_list = self._find_bahamut_weapon_appiled_race(reg_list, CharacterRace.doraf)

        hl_list = self._create_hl_weapon_all()
        hl_list = self._find_bahamut_weapon_appiled_race(hl_list, CharacterRace.doraf)

        for weapon in reg_list:
            self.assertTrue(weapon.weapon_type in reg_pass)

        for weapon in hl_list:
            self.assertTrue(weapon.weapon_type in hl_pass)

    def test_bahamut_erun(self):
        reg_pass = ['spear', 'staff']
        hl_pass = ['dagger', 'spear', 'staff']

        reg_list = self._create_weapon_all()
        reg_list = self._find_bahamut_weapon_appiled_race(reg_list, CharacterRace.erun)

        hl_list = self._create_hl_weapon_all()
        hl_list = self._find_bahamut_weapon_appiled_race(hl_list, CharacterRace.erun)

        for weapon in reg_list:
            self.assertTrue(weapon.weapon_type in reg_pass)

        for weapon in hl_list:
            self.assertTrue(weapon.weapon_type in hl_pass)

    def test_bahamut_harvin(self):
        reg_pass = ['gun', 'staff']
        hl_pass = ['axe', 'gun', 'staff']

        reg_list = self._create_weapon_all()
        reg_list = self._find_bahamut_weapon_appiled_race(reg_list, CharacterRace.harvin)

        hl_list = self._create_hl_weapon_all()
        hl_list = self._find_bahamut_weapon_appiled_race(hl_list, CharacterRace.harvin)

        for weapon in reg_list:
            self.assertTrue(weapon.weapon_type in reg_pass)

        for weapon in hl_list:
            self.assertTrue(weapon.weapon_type in hl_pass)
