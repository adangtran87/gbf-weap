import context
import unittest

from weapon import *
from weapon_pool import WeaponPool
from summon import Summon, SummonType
from character import CharacterRace, Character

class TestWeaponPool(unittest.TestCase):
    def setUp(self):
        wep_list = [
                    'normal', 'normal2', 'unknown', 'strength',
                    'magna', 'magna', 'magna', 'magna',
                    ('bahamut', 'sword'), ('hl_bahamut', 'dagger'),
                   ]
        self.weapon_pool = self._create_pool_from_list(wep_list)

        self.summon_none = Summon("none", 'elemental', 0.0);
        self.summon_elemental = Summon("elemental", 'elemental', 0.5)
        self.summon_magna = Summon('magna', 'magna', 0.5)
        self.summon_ranko = Summon('ranko', 'ranko', 0.5)
        self.summon_primal = Summon('primal', 'primal', 0.5)
        self.summon_character = Summon('character', 'character', 0.5)

        self.normal_mod = self.weapon_pool.normal_modifier
        self.magna_mod = self.weapon_pool.magna_modifier
        self.unknown_mod = self.weapon_pool.unknown_modifier
        self.strength_mod = self.weapon_pool.strength_modifier
        self.bahamut_mod = self.weapon_pool.bahamut_modifier

        self.character = Character("test", [], 'unknown')

        pass
    def tearDown(self):
        pass

    def _create_pool_from_list(self, wep_type_list):
        pool_list = []
        for index, wep_type in enumerate(wep_type_list):
            if isinstance(wep_type, tuple):
                if (wep_type[0] == 'bahamut'):
                    weapon = WeaponBahamut(**{
                                'name': index,
                                'weapon_class': "bahamut",
                                'damage': 1000,
                                'weapon_type': wep_type[1],
                                'skill_level': 10
                                })
                elif (wep_type[0] == 'hl_bahamut'):
                    weapon = WeaponHLBahamut(**{
                                'name': index,
                                'weapon_class': "hl_bahamut",
                                'damage': 1000,
                                'weapon_type': wep_type[1],
                                'skill_level': 10
                                })
            else:
                if (wep_type == 'normal'):
                    weapon = WeaponNormal(**{
                                'name': index,
                                'weapon_class': "normal",
                                'damage': 1000,
                                'weapon_type': 'sword',
                                'weapon_skill': 'large',
                                'skill_level': 10
                                })
                elif (wep_type == 'normal2'):
                    weapon = WeaponNormal2(**{
                                'name': index,
                                'weapon_class': "normal2",
                                'damage': 1000,
                                'weapon_type': 'sword',
                                'weapon_skill': 'large',
                                'skill_level': 10
                                })
                elif (wep_type == 'magna'):
                    weapon = WeaponMagna(**{
                                'name': index,
                                'weapon_class': "magna",
                                'damage': 1000,
                                'weapon_type': 'sword',
                                'weapon_skill': 'large',
                                'skill_level': 10
                                })
                elif (wep_type == 'unknown'):
                    weapon = WeaponUnknown(**{
                                'name': index,
                                'weapon_class': "unknown",
                                'damage': 1000,
                                'weapon_type': 'sword',
                                'weapon_skill': 'large',
                                'skill_level': 10
                                })
                elif (wep_type == 'strength'):
                    weapon = WeaponStrength(**{
                                'name': index,
                                'weapon_class': "strength",
                                'damage': 1000,
                                'weapon_type': 'sword',
                                'weapon_skill': 'large',
                                'skill_level': 10
                                })
            pool_list.append(weapon)
        return WeaponPool(pool_list)

    def test_weapon_pool_base_damage(self):
        self.assertEqual(self.weapon_pool.base_damage, 10000)

    def test_weapon_pool_normal_mod(self):
        # 1 Normal sl 10 = 15
        # 1 normal sl 10 = 16
        self.assertEqual(self.normal_mod, 0.31)

    def test_weapon_pool_magna_mod(self):
        # 4 Magna sl 10 = 4*15 = 0.60
        self.assertEqual(self.magna_mod, 0.60)

    def test_weapon_pool_unknown_mod(self):
        # 1 Unknown sl 10 = .15
        self.assertEqual(self.unknown_mod, 0.15)

    def test_weapon_pool_strength_mod(self):
        # 1 strength sl 10 = .15
        self.assertEqual(self.strength_mod, 0.15)

    def test_weapon_pool_bahamut_mod(self):
        # 1 bahamut sword sl 10 = .15
        # 1 hl bahamut dagger sl 10 = .30
        self.assertEqual(self.bahamut_mod, 0.45)

    # Test weapon_pool.calc_damage()
    def test_weapon_pool_calc_damage_none_none(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_none, self.summon_none, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_ele_none(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0.5)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_elemental, self.summon_none, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_ele_ele(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0.5 + 0.5)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_elemental, self.summon_elemental, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_magna_none(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0.5))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_magna, self.summon_none, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_magna_magna(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0.5+0.5))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_magna, self.summon_magna, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_ranko_none(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0.5)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_ranko, self.summon_none, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_ranko_ranko(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0.5+0.5)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_ranko, self.summon_ranko, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_primal_none(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0.5)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_primal, self.summon_none, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_primal_primal(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0.5+0.5)) + self.bahamut_mod + 0) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_primal, self.summon_primal, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_character_none(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0.5) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_character, self.summon_none, self.character)
        self.assertEqual(pool_damage, expected_damage)

    def test_weapon_pool_calc_damage_character_character(self):
        # All modifiers tested above so can depend on them.
        expected_damage = round(
                           (10000 *
                           (1 + (self.normal_mod * (1+0)) + self.bahamut_mod + 0.5+0.5) *
                           (1 + (self.magna_mod * (1+0))) *
                           (1 + (self.unknown_mod * (1+0)) + self.strength_mod) *
                           (1 + 0)),
                           2
                          )
        pool_damage = self.weapon_pool.calc_damage(self.summon_character, self.summon_character, self.character)
        self.assertEqual(pool_damage, expected_damage)
