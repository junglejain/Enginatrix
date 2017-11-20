from numpy.random import randint
from src.game.core.Rating import Rating


class Stat(Rating):

    def __init__(self, data):
        self.fumble = data['fumble']
        self.crit = data['crit']
        self.crit_over = data['crit_over']
        self.to_raise = data['to_raise']
        self.to_lower = data['to_lower']
        self.raise_message = data['raise_message']
        self.lower_message = data['lower_message']
        self.easy = data['easy']
        self.can_lower = data['can_lower']
        self.last_use = data['last_use']
        self.mod = 0

        super().__init__(data)

    def __repr__(self):
        return 'Stat(%s)' % self.name+': '+str(self.val)+'+'+str(self.mod)+'/'+str(self.max)

    def add_mod(self, val):
        """Add a modifier to the stat for rolling. The passed value is added directly to the current value.
          Pass a negative for a negative modifier!"""
        self.mod += val

    def roll(self, diff, mod=0):
        """A roll is considered 'pass' if random (0-max) plus current, plus mods > difficulty.
        so Strength 10, max 20, mods +2, difficulty 15: random(0-20)+10+2 > 15?
        A passed mod is a modifier used for this single roll only, added to any current permanent mods"""
        self.last_use = 0
        start = randint(0, self.max)
        if self.fumble and start == 0:
            return -1
        if self.crit and self.crit_over == 0 and start == self.max:
            return 2
        total = start + self.val + self.mod + mod
        if self.crit and self.crit > 0 and total > diff*self.crit_over:
            return 2
        if total > diff:
            return 1
        return 0

    def check_raise(self):
        self.last_use = 0
        self.to_raise += 1
        if (not self.easy and self.to_raise >= 20) or (self.easy and self.to_raise >= 5):
            self.to_raise = 0
            self.val += 1
            return True
        return False

    def check_lower(self):
        if self.can_lower and self.last_use >= 10:
            self.to_lower += 1
            self.last_use = 0
            if self.to_lower >= 20:
                if self.to_raise > 0:
                    self.to_raise = 0
                else:
                    self.val -= 1
                return True
        elif self.can_lower:
            self.last_use += 1
        return False
