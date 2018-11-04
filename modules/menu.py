class Menu:
    def __init__(self):
        self.options = []
        self.active = 0

    def next(self):
        if self.active < len(self.options):
            self.active += 1
        else: 
            self.active = 0

    def previous(self):
        if self.active > 0:
            self.active -= 1
        else:
            self.active = len(self.options) - 1

    def get_active(self):
        return self.options[self.active]


class Option:
    def __init__(self, label="Option", value=0, action=None):
        self.label = label
        self.action = action
        self.value = 0

    def execute(self):
        self.action()


class List(Menu):
    def __init__(self, label="List"):
        Menu.__init__(self)
        self.label = label
    def execute(self):
        self.get_active().execute()

