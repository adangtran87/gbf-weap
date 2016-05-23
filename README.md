# gbf-weap
This script tries to find the optimum weapon pool from a list of weapons and
list of summon pairs. The script optimizes for attack/damage.

### How To Run
`python weapon-optimizer.py [-h] [--list_all] config`

`python weapon-optimizer.py fire.json`

### Running Unit Tests
`python -m unittest discover tests`

### Limitations
* Only considering 'attack' weapon skills
  * Does not consider last stand attack modifiers
* List of weapons and summons must have weapon skills of the same element
  * Weapon and summon lists must be in json format
  * Stat sticks should have a skill type of 'none'
* Assumes character race for bahamut weapons is unknown
* Does not take weapon preference into account
* Current algorithm brute forces all weapon pool combinations
  * Beware long weapon lists; have not tested limits

### References/Thanks
[Ajantus's GBF Weapon/Summon Optimization](http://gbf-english.proboards.com/thread/595/#6)

### Toolchain
* Python 2.7
* enum34
* Should be compatible with Python 3.4 but not continuously run

### JSON enum strings
##### Weapon Class
* normal, normal2, magna, unknown, strength, bahamut, stat_stick

##### Weapon Type
* sword, dagger, spear, axe, staff, gun, fist, bow, harp, katana

##### Weapon Skills (normal, normal2, magna, unknown, strength)
* none, small, medium, large

##### Summon Type
* elemental, magna, primal, ranko, character

