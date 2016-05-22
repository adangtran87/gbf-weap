import context
import unittest

from weapon import *

class TestNormalClass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _create_weapon(self, name, damage, weapon_skill, skill_level):
        return WeaponNormal(**{
                                'name':name,
                                'weapon_class':"normal",
                                'damage':damage,
                                'weapon_type':'sword',
                                'weapon_skill': weapon_skill,
                                'skill_level':skill_level
                                }
                            )
    #Tests according to section 5.1 of http://gbf-english.proboards.com/thread/595/
    def test_normal_small_multipliers(self):
        pass_mult = [0.01, 0.02, 0.03, 0.04, 0.05,
                     0.06, 0.07, 0.08, 0.09, 0.10,
                     0.104, 0.108, 0.112, 0.116, 0.12]

        for skill_level in range(0,15):
            weapon = self._create_weapon(skill_level, 1000, 'small', skill_level+1)
            self.assertEqual(weapon.multiplier, pass_mult[skill_level])

    def test_normal_medium_multipliers(self):
        pass_mult = [0.03, 0.04, 0.05, 0.06, 0.07,
                     0.08, 0.09, 0.10, 0.11, 0.12]

        for skill_level in range(0,15):
            try:
                weapon = self._create_weapon(skill_level, 1000, 'medium', skill_level+1)
                self.assertEqual(weapon.multiplier, pass_mult[skill_level])
            except:
                if skill_level > 9:
                    success = True
                else:
                    success = False
                self.assertTrue(success)

    def test_normal_large_multiplier(self):
        pass_mult = [0.06, 0.07, 0.08, 0.09, 0.10,
                     0.11, 0.12, 0.13, 0.14, 0.15,
                     0.156, 0.162, 0.168, 0.174, 0.18]

        for skill_level in range(0,15):
            weapon = self._create_weapon(skill_level, 1000, 'large', skill_level+1)
            self.assertEqual(weapon.multiplier, pass_mult[skill_level])
