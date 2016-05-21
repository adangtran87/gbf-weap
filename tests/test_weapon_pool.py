import context
import unittest

from weapon import *
from weapon_pool import WeaponPool

class TestWeaponPool(unittest.TestCase):
    def setUp(self):
        wep_list = [ 'normal', 'normal2', 'unknown',
                     'magna', 'magna', 'magna', 'magna', 'magna',
                     ('bahamut', 'sword'), ('hl_bahamut', 'dagger'),
                   ]
        self.weapon_pool = self._create_pool_from_list(wep_list)
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
            pool_list.append(weapon)
        return WeaponPool(pool_list)

    def test_weapon_pool_base_damage(self):
        self.assertEqual(self.weapon_pool.base_damage, 10000)

    def test_weapon_pool_normal_mod(self):
        # 1 Normal sl 10 = 15
        # 1 normal sl 10 = 16
        self.assertEqual(self.weapon_pool.normal_modifier, 0.31)

    def test_weapon_pool_magna_mod(self):
        # 5 Magna sl 10 = 5*15 = 0.75
        self.assertEqual(self.weapon_pool.magna_modifier, 0.75)

    def test_weapon_pool_unknown_mod(self):
        # 1 Unknown sl 10 = .15
        self.assertEqual(self.weapon_pool.unknown_modifier, 0.15)

    def test_weapon_pool_bahamut_mod(self):
        # 1 bahamut sword sl 10 = .15
        # 1 hl bahamut dagger sl 10 = .30
        self.assertEqual(self.weapon_pool.bahamut_modifier, 0.45)
