from numpy.random import normal
from src.game.core.Database import Database
from src.game.core.Messages import Messages


class Orifice(object):
    """These are not normal measurements.  This is a fantasy game, and people don't want 5 inches to be the average
        penis size in their fantasy games, so I greatly increased normal vaginal length and width (and the standard
        deviation) and wildly over-estimated stretchability and arousal changes.  Also simplified centimeter to inch
        conversion to 2.5 for sanity's sake."""

    db = Database()
    message = Messages()

    length_mean = 20                # 8 inches
    length_sd = 7.5                 # 5-11 inches
    width_mean = 7.5                # 3 inches
    width_sd = 5                    # 1-5 inches

    max_length_stretch = 2.5        # 6-12 inches long total
    max_width_stretch = 5           # 3-7 inches wide total

    max_length_wet = 2.5            # 7-13 inches long
    max_width_wet = 5               # 5-9 inches wide

    max_length_train = 5            # 9-15 long
    max_width_train = 7.5           # 8-12 wide

    def __init__(self, char, o_type):
        self.character = char
        self.o_type = o_type

        if self.character.id > 0:
            self.length, self.width = self.db.get_tup(
                """select length, width from Char_Orifice where char_id=? and type=?""",
                [self.character.id, self.o_type]
            )
        else:
            self.width = 0
            self.length = 0

        if not self.length or not self.width:
            self.length = normal(self.length_mean, self.length_sd)
            self.width = normal(self.width_mean, self.width_sd)
            self.save()

    def arousal_length(self):
        # Arousal is actually arousal - stress:
        arousal = self.character.arousal - self.character.stress
        if arousal < 0:
            arousal = 0
        return (self.max_length_wet / self.character.arousal.max) * arousal

    def arousal_width(self):
        # Arousal is actually arousal - stress:
        arousal = self.character.arousal - self.character.stress
        if arousal < 0:
            arousal = 0
        return (self.max_width_wet / self.character.arousal.max) * arousal

    def train_length(self):
        return (self.max_length_train / self.character.intercourse.max) * self.character.intercourse

    def train_width(self):
        return (self.max_width_train / self.character.intercourse.max) * self.character.intercourse

    def endurance_width(self):
        return (self.max_width_train / self.character.endurance.max) + self.character.endurance

    def endurance_length(self):
        return (self.max_length_train / self.character.endurance.max) + self.character.endurance

    def base_stimulation(self, implement, depth='normal'):
        i_length = implement.length
        if depth == 'hard':
            i_length = i_length * 1.2
        elif depth == 'soft':
            i_length = i_length * .8

        arousal_width = self.width+self.arousal_width()
        train_width = arousal_width+self.train_width()
        stretch_width = train_width+self.max_width_stretch
        endurance_width = stretch_width+self.endurance_width()

        train_length = self.length+self.arousal_length()+self.train_length()
        stretch_length = train_length+self.max_length_stretch
        endurance_length = stretch_length+self.endurance_length()

        # Length only matters if it's too big.
        width_stim = 0
        stress = 0
        # Width under base is pointless.
        # Width between base and arousal is okay:
        if self.width <= implement.width < arousal_width:
            width_stim = 3
        # Between arousal and training is perfect:
        if arousal_width <= implement.width < train_width:
            width_stim = 5
        # Between training and stretch is okay, again, and furthers training:
        if train_width <= implement.width < stretch_width:
            width_stim = 3
            self.character.intercourse.check_raise()
        # Past max stretch gets into endurance training:
        if stretch_width <= implement.width < endurance_width:
            # If you're a masochist, this is perfect:
            if self.character.hasFetish('Masochist'):
                width_stim = 5
        # Past stretch and endurance, this is a negative, but trains endurance:
        if implement.width >= endurance_width:
            width_stim = -5
            stress += 5
            self.character.endurance.check_raise()

        length_stim = 0

        if train_length <= i_length < stretch_length:
            self.character.intercourse.check_raise()
        if stretch_length <= i_length < endurance_length:
            if self.character.hasFetish('Masochist'):
                length_stim = 5
        if i_length >= endurance_length:
            length_stim = -5
            stress += 5
            self.character.endurance.check_raise()

        return width_stim+length_stim, stress

    def save(self):
        self.db.save(
            """INSERT INTO Char_Orifice (char_id, length, width, type) VALUES (?,?,?,?)""",
            [self.character, self.length, self.width, self.o_type]
        )
