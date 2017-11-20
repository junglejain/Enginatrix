from src.game.core.Database import Database
from src.game.core.Rating import Rating
from src.game.model.Stat import Stat


class Character(object):

    db = Database()
    attrs = db.get_table('Attributes')
    skills = db.get_table('Skills')
    specs = db.get_table('Special')
    stims = db.get_table('Stimulation')

    attr_default = {'s_max': 20, 'fumble': True, 'crit': True, 'crit_over': 0, 'easy': False, 'can_lower': True}
    attr_new = {'s_val': 10, 'to_raise': 0, 'to_lower': 0, 'last_use': 0}

    skill_default = {'s_max': 100, 'fumble': True, 'crit': True, 'crit_over': 0, 'to_lower': 0, 'lower_message': "",
                     'easy': True, 'can_lower': False}
    skill_new = {'s_val': 20, 'to_raise': 0, 'last_use': 0}

    spec_default = {'s_max': 100}
    spec_new = {'s_val': 0}

    def __init__(self, c_id=0, pc=False):
        loads = self.load_char(c_id, pc)
        for key, value in loads:
            setattr(self, key, value)

    def load_char(self, c_id, pc):
        if not c_id:
            return self.empty_char(pc)

        loads = self.db.get_row('Char', c_id)

        for attr in self.attrs:
            add = {
                's_name': attr['name'],
                'raise_message': attr['raise_message'],
                'lower_message': attr['lower_message']
            }
            add.update(self.db.get_one(
                "Select s_val, to_raise, to_lower, last_use from Char_Attr where char_id=? and attr_id=?",
                (c_id, attr['id']))
            )
            loads[str.lower(attr['name'])] = Stat({**self.attr_default, **add})

        for skill in self.skills:
            add = {
                's_name': skill['name'],
                'raise_message': skill['raise_message']
            }
            add.update(self.db.get_one(
                "Select s_val, to_raise, last_use from Char_Skills where char_id=? and skill_id=?", (c_id, skill['id']))
            )
            loads[str.lower(skill['name'])] = Stat({**self.skill_default, **add})

        for spec in self.specs:
            if spec['npc_only'] and pc:
                continue
            add = {
                's_name': spec['name']
            }
            add.update(self.db.get_one("Select s_val from Char_Spec where char_id=? and spec_id=?", (c_id, spec['id'])))
            loads[str.lower(spec['name'])] = Rating({**self.spec_default, **add})

        for stim in self.stims:
            add = {
                's_name': stim['name']
            }
            add.update(self.spec_new)
            loads[str.lower(stim['name'])] = Rating({**self.spec_default, **add})

        return loads

    def empty_char(self, pc):
        loads = {}

        table = self.db.def_table('Char')
        for row in table:
            if row[2] is 'INTEGER' or row[2] is 'INT':
                loads[row[1]] = 0
            else:
                loads[row[1]] = ''

        for attr in self.attrs:
            add = {
                's_name': attr['name'],
                'raise_message': attr['raise_message'],
                'lower_message': attr['lower_message']
            }
            add.update(self.attr_new)
            loads[str.lower(attr['name'])] = Stat({**self.attr_default, **add})

        for skill in self.skills:
            add = {
                's_name': skill['name'],
                'raise_message': skill['raise_message']
            }
            add.update(self.skill_new)
            loads[str.lower(skill['name'])] = Stat({**self.skill_default, **add})

        for spec in self.specs:
            if spec['npc_only'] and pc:
                continue
            add = {
                's_name': spec['name']
            }
            add.update(self.spec_new)
            loads[str.lower(spec['name'])] = Rating({**self.spec_default, **add})

        for stim in self.stims:
            add = {
                's_name': stim['name']
            }
            add.update(self.spec_new)
            loads[str.lower(stim['name'])] = Rating({**self.spec_default, **add})

        return loads
