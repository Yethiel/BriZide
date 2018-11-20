from bge import logic, events
import math

kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

class Layout:
    def __init__(self, game_obj):
        self.elements = []
        self.go = game_obj
        self.sce = self.go.scene

    def run(self):
        for element in self.elements:
            element.run()

    def hide(self):
        for element in self.elements:
            element.hide()

    def show(self):
        for element in self.elements:
            element.show()


class Menu:
    def __init__(self, game_obj, focused=False):
        """ Creates a menu 
            
                game_obj: 
                    A game object that will be used as the root of the menu
        """
        self.options = []
        self.active = 0

        self.go = game_obj
        self.sce = self.go.scene
        self.focused = focused

    def next(self):
        if self.active < len(self.options)-1:
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

    def set_active(self, option_name):
        for opt in self.options:
            if opt.text == option_name:
                self.active = self.options.index(opt)

    def hide(self):
        for option in self.options:
            option.hide()

    def show(self):
        for option in self.options:
            option.show()

    def focus(self):
        self.focused = True
        self.go["timer"] = 0.0

    def unfocus(self):
        self.focused = False

    def populate(self, texts=[], position=[0.0, 0.0, 0.0], size=1.0, actions=[], hidden=False):
        for i in range(len(texts)):
            text = texts[i]
            pos = position
            pos[1] -= size
            opt = Option(
                self, text=text, position=pos, size=size, value=i, action=actions[i], hidden=hidden
            )
            self.options.append(opt)

    def run(self):
        self.controls()

        for i in range(len(self.options)):
            self.options[i].go.color = [0.3, 0.3, 0.2, 1.0]
            if i == self.active:
                c = math.sin(self.go["timer"]*8) / 4
                self.options[i].go.color = [0.75 + c, 0.75 + c, 0.65 + c, 1.0]
            self.options[i].run()

    def controls(self):
        if logic.uim.focus == "menu" and self.focused and self.go["timer"] > 0.1:
            if kbd.events[events.UPARROWKEY] == JUST_ACTIVATED:
                self.previous()
            if kbd.events[events.DOWNARROWKEY] == JUST_ACTIVATED:
                self.next()
            if kbd.events[events.ENTERKEY] == JUST_ACTIVATED:
                self.get_active().execute()


class Option:
    def __init__(self, parent=None, text="Option", position=[0.0, 0.0, 0.0], size=1.0, value=0, action=None, update=None, hidden=False):
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
        self.update = update
        self.value = 0

        self.go = self.parent.sce.addObject("ui_label", parent.go)
        self.go.worldPosition = position
        self.go.size = size

        if hidden:
            self.hide()

    def hide(self):
        self.go.visible = False

    def show(self):
        self.go.visible = True

    def run(self):
        if self.update is not None:
            self.update(self)
        self.go.text = self.text

    def execute(self):
        self.action(self)


class List(Menu):
    def __init__(self, label="List"):
        Menu.__init__(self)
        self.label = label
    def execute(self):
        self.get_active().execute()

