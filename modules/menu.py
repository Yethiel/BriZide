from bge import logic, events

kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

class Menu:
    def __init__(self, game_obj):
        """ Creates a menu 
            
                game_obj: 
                    A game object that will be used as the root of the menu
        """
        self.options = []
        self.active = 0

        self.sce = logic.getCurrentScene()
        self.go = game_obj

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

    def update(self):

        self.controls()

        for i in range(len(self.options)):
            if i == self.active:
                self.options[i].color = [1.0, 0.0, 0.0, 0.0]
            self.options[i].update()


    def controls(self):
        if kbd.events[events.UPARROWKEY] == JUST_RELEASED:
            self.previous()
        if kbd.events[events.DOWNARROWKEY] == JUST_RELEASED:
            self.next()




class Option:
    def __init__(self, parent=None, text="Option", position=[0.0, 0.0, 0.0], value=0, action=None):
        """ Creates a menu option
            parent:
                Parent UI element
            text:
                Text for the option
            value:
                Internal value of the option
            action:
                Function that's executed when the option is selected
        """
        self.parent = parent
        self.text = text
        self.action = action
        self.value = 0

        self.go = self.parent.sce.addObject("ui_label", parent.go)
        self.go.worldPosition = position

    def update(self):
        self.go.text = self.text

    def execute(self):
        self.action()


class List(Menu):
    def __init__(self, label="List"):
        Menu.__init__(self)
        self.label = label
    def execute(self):
        self.get_active().execute()

