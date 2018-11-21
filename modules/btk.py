from bge import logic, events
import math

kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

class Layout:
    def __init__(self, title, game_obj):
        """ A container for elements
            title:
                String: identifier of the layout
            game_obj:
                KX_GameObject
        """
        self.title = title
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

    def add_element(self, element):
        self.elements.append(element)

    def remove_element(self, element):
        self.elements.remove(element)

    def get_element(self, title):
        for element in self.elements:
            if element.title == title:
                return element
        return None


class Menu(Layout):
    def __init__(self, title, parent, focused=False):
        """ Creates a menu 
                title:
                    String: Identifier of the Menu
                parent: 
                    Layout: The Parent UI Element
                focused:
                    Boolean: Whether the menu gains control
        """

        super().__init__(title, parent.go)
        self.parent = parent
        self.active = 0
        self.focused = focused
        self.parent.add_element(self)

    def next(self):
        if self.active < len(self.elements)-1:
            self.active += 1
        else: 
            self.active = 0

    def previous(self):
        if self.active > 0:
            self.active -= 1
        else:
            self.active = len(self.elements) - 1

    def get_active(self):
        return self.elements[self.active]

    def set_active(self, option_name):
        for opt in self.elements:
            if opt.text == option_name:
                self.active = self.elements.index(opt)

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

    def run(self):
        self.controls()

        for i in range(len(self.elements)):
            self.elements[i].go.color = [0.3, 0.3, 0.2, 1.0]
            if i == self.active:
                c = math.sin(self.go["timer"]*8) / 4
                self.elements[i].go.color = [0.75 + c, 0.75 + c, 0.65 + c, 1.0]
            self.elements[i].run()

    def controls(self):
        if logic.uim.focus == "menu" and self.focused and self.go["timer"] > 0.1:
            if kbd.events[events.UPARROWKEY] == JUST_ACTIVATED:
                self.previous()
            if kbd.events[events.DOWNARROWKEY] == JUST_ACTIVATED:
                self.next()
            if kbd.events[events.ENTERKEY] == JUST_ACTIVATED:
                self.get_active().execute()

class Element:
    def __init__(self, parent, object, position, update=None, hidden=False):
        self.parent = parent
        self.update = update
        self.go = self.parent.sce.addObject(object, parent.go)
        self.go.worldPosition = position

        self.parent.add_element(self)

        if hidden:
            self.hide()

    def run(self):
        if self.update is not None:
            self.update(self)

    def hide(self):
        self.go.visible = False

    def show(self):
        self.go.visible = True


class Label(Element):
    def __init__(self, parent, text="Label", position=[0.0, 0.0, 0.0], size=1.0, update=None, hidden=False):
        super().__init__(parent, "ui_label", position, update, hidden)
        self.text = text
        self.go.size = size

    def set_color(self, color):
        self.go.color = color

    def run(self):
        super().run()
        self.go.text = self.text


class Option(Label):
    def __init__(self, parent, text="Option", position=[0.0, 0.0, 0.0], size=1.0, value=0, action=None, update=None, hidden=False):
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
        super().__init__(parent, text=text, position=position, size=size, update=update, hidden=hidden)
        self.action = action
        self.value = 0

    def execute(self):
        self.action(self)
