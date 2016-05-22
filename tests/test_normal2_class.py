import context
import unittest

from weapon import *

class TestNormal2Class(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _create_weapon(self, name, damage, weapon_skill, skill_level):
        return WeaponNormal2(**{
                                'name':name,
                                'weapon_class':"normal2",
                                'damage':damage,
                                'weapon_type':'sword',
                                'weapon_skill': weapon_skill,
                                'skill_level':skill_level
                                }
                            )
    def test_normal2_large_multiplier(self):
        pass_mult = [0.07, 0.08, 0.09, 0.10, 0.11,
                     0.12, 0.13, 0.14, 0.15, 0.16,
                     0.168, 0.176, 0.184, 0.192, 0.20]

        for skill_level in range(0,15):
            weapon = self._create_weapon(skill_level, 1000, 'large', skill_level+1)
            self.assertEqual(weapon.multiplier, pass_mult[skill_level])
