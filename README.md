# gbf-weap
This script tries to find the optimum weapon pool from a list of weapons and
list of summon pairs. The script optimizes for attack/damage.

### How To Run
`python weapon-optimizer.py [-h] [--list_all] weapons summons`

`python weapon-optimizer.py fire-weapons.json fire-summons.json`

### Limitations
* Only considering 'attack' weapon skills
  * Does not consider last stand attack modifiers
* List of weapons and summons must have weapon skills of the same element
  * Weapon and summon lists must be in json format
  * Stat sticks should have a skill type of 'none'
* Assumes that bahamut weapon is **on race**
  * Does **not** support sword, staff
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
##### Weapon Type
* normal
* magna
* unknown
* bahamut
* strength

##### Weapon Skills
* none
* small
* medium
* large

##### Summon Type
* elemental
* magna
* primal
* ranko
* character

