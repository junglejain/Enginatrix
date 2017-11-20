class Messages(object):
    bad_messages = []
    info_messages = []
    good_messages = []

    def __init__(self):
        pass

    def bad(self, message):
        self.bad_messages.append(message)

    def info(self, message):
        self.info_messages.append(message)

    def good(self, message):
        self.good_messages.append(message)
