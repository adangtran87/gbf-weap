# gbf-weap
This script tries to find the optimum weapon pool from a list of weapons and
list of summon pairs. The script optimizes for attack/damage.

#### JSON enum strings
##### Weapon Type
* normal
* magna
* unknown
* bahamut

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

#### Limitations
* List of weapons and summons must have weapon skills of the same element
  * Weapon and summon lists must be in json format
  * Stat sticks should have a skill type of 'none'
* Only considering 'attack' weapon skills
  * Does not consider last stand attack modifiers
* Does not take weapon preference into account
* Current algorithm brute forces all weapon pool combinations
  * Beware long weapon lists; have not tested limits

#### References
[Ajantus's GBF Weapon/Summon Optimization](http://gbf-english.proboards.com/thread/595/#6)


### Toolchain
* Python 2.7
* enum34
* Should be compatible with Python 3.4 but not continuously run

### How To Run
`python weapon-optimizer.py -s fire-summons.json -w fire-weapons.json`
