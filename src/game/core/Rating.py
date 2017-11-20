class Rating(object):

    def __init__(self, data):
        self.name = data['s_name']
        self.max = data['s_max']
        self.val = data['s_val']

    def __setattr__(self, key, value):
        """Set boundries on maximum and current value."""
        if key is 'val':
            if value < 0:
                value = 0
            elif value > self.max:
                value = self.max
        elif key is 'max':
            if value < 1:
                value = 1
        super().__setattr__(key, value)

    def __lt__(self, val):
        if isinstance(val, Rating):
            return self.val < val.val
        elif isinstance(val, (int, float)):
            return self.val < val
        else:
            return NotImplemented

    def __le__(self, val):
        if isinstance(val, Rating):
            return self.val <= val.val
        elif isinstance(val, (int, float)):
            return self.val <= val
        else:
            return NotImplemented

    def __eq__(self, val):
        if isinstance(val, Rating):
            return self.val == val.val
        elif isinstance(val, (int, float)):
            return self.val == val
        else:
            return NotImplemented

    def __ne__(self, val):
        if isinstance(val, Rating):
            return self.val != val.val
        elif isinstance(val, (int, float)):
            return self.val != val
        else:
            return NotImplemented

    def __gt__(self, val):
        if isinstance(val, Rating):
            return self.val > val.val
        elif isinstance(val, (int, float)):
            return self.val > val
        else:
            return NotImplemented

    def __ge__(self, val):
        if isinstance(val, Rating):
            return self.val >= val.val
        elif isinstance(val, (int, float)):
            return self.val >= val
        else:
            return NotImplemented

    def __add__(self, val):
        if isinstance(val, Rating):
            return self.val + val.val
        elif isinstance(val, (int, float)):
            return self.val + val
        else:
            return NotImplemented

    def __sub__(self, val):
        if isinstance(val, Rating):
            return self.val - val.val
        elif isinstance(val, (int, float)):
            return self.val - val
        else:
            return NotImplemented

    def __bool__(self):
        if not isinstance(self.val, int) or self.val < 0:
            return False
        return True

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return 'Rating(%s)' % self.name+': '+str(self.val)+'/'+str(self.max)

    def percent(self):
        """Returns current percentage ([current / max] * 100)"""
        return int(round((self.val / self.max) * 100))
