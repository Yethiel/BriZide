"""
BTK: A GUI toolkit for the Blender Game Engine
"""

from bge import logic, events, render
import math
from modules import sound
from modules.helpers import clamp

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
                KX_GameObject to use as the root
        """
        self.title = title
        self.elements = []
        self.root = game_obj
        self.sce = self.root.scene

    def run(self):
        for element in self.elements:
            element.run()

    def hide(self):
        for element in self.elements:
            element.hide()

    def end(self):
        for element in self.elements:
            if hasattr(element, "go"):
                print("Ending game object")
                element.go.endObject()
            if hasattr(element, "elements"):
                print("Ending menu")
                element.end()

    def show(self):
        for element in self.elements:
            element.show()

    def unfocus(self):
        for element in self.elements:
            if hasattr(element, "unfocus"):
                element.unfocus()

    def add_element(self, element):
        self.elements.append(element)

    def remove_element(self, element):
        self.elements.remove(element)

    def get_element(self, title):
        for element in self.elements:
            if hasattr(element, "title") and element.title == title:
                return element
        return None


class Menu(Layout):
    def __init__(self, title, parent, focused=False, select_callback=None):
        """ Creates a menu 
                title:
                    String: Identifier of the Menu
                parent: 
                    Layout: The Parent UI Element
                focused:
                    Boolean: Whether the menu gains control
        """

        super().__init__(title, parent.root)
        self.parent = parent
        self.active = 0
        self.focused = focused
        self.parent.add_element(self)
        self.size = 1.0
        self.select_callback = select_callback

    def set_element_color(self, element):
        element.go.color[3] = 1 - abs(self.elements.index(self.get_active()) - self.elements.index(element)) / len(self.elements)

    def next(self):
        if self.active < len(self.elements)-1:
            self.active += 1
            for e in self.elements:
                e.go.worldPosition[1] += self.size
                self.set_element_color(e)
        else: 
            self.active = 0
            for e in self.elements:
                e.go.worldPosition[1] += self.size
                e.go.worldPosition[1] -= self.size * len(self.elements)
                self.set_element_color(e)

    def previous(self):
        if self.active > 0:
            self.active -= 1
            for e in self.elements:
                e.go.worldPosition[1] -= self.size
                self.set_element_color(e)
        else:
            self.active = len(self.elements) - 1
            for e in self.elements:
                e.go.worldPosition[1] -= self.size
                e.go.worldPosition[1] += self.size * len(self.elements)
                self.set_element_color(e)


    def get_active(self):
        return self.elements[self.active]

    def set_active(self, option_name):
        for opt in self.elements:
            if opt.text == option_name:
                self.active = self.elements.index(opt)

    def focus(self):
        self.focused = True
        self.root["ui_timer"] = 0.0

    def unfocus(self):
        self.focused = False

    def populate(self, texts=[], position=[0.0, 0.0, 0.0], size=1.0, actions=[], updates=None, hidden=False):
        self.size = size
        if updates is None:
            updates = [None for x in range(len(texts))]
        for i in range(len(texts)):
            text = texts[i]
            pos = position
            pos[1] -= size
            opt = Option(
                self, text=text, position=pos, size=size, value=i, action=actions[i], update=updates[i], hidden=hidden
            )
        for e in self.elements:
            self.set_element_color(e)

    def run(self):
        self.controls()

        for i in range(len(self.elements)):
            self.elements[i].go.color[0] = 0.3
            self.elements[i].go.color[1] = 0.3
            self.elements[i].go.color[2] = 0.2
            if i == self.active:
                c = math.sin(self.root["ui_timer"]*8) / 4
                self.elements[i].go.color = [0.75 + c, 0.75 + c, 0.65 + c, 1.0]
            self.elements[i].run()

    def controls(self):
        if self.focused and self.root["ui_timer"] > 0.1:  #logic.uim.focus == "menu"
            if kbd.events[events.UPARROWKEY] == JUST_ACTIVATED:
                self.previous()
                sound.play("menu")
                if self.select_callback:
                    self.select_callback(self)
            if kbd.events[events.DOWNARROWKEY] == JUST_ACTIVATED:
                self.next()
                sound.play("menu")
                if self.select_callback:
                    self.select_callback(self)
            if kbd.events[events.ENTERKEY] == JUST_ACTIVATED:
                sound.play("select")
                self.get_active().execute()


class Element:
    def __init__(self, parent, object=None, position=[0,0,0], scale=[1,1,1], title="", update=None, hidden=False):
        self.parent = parent
        self.update = update
        self.go = self.parent.sce.addObject(object, parent.root)
        self.go.worldPosition = position
        self.go.worldScale = scale
        self.title = title
        self.parent.add_element(self)

        if hidden:
            self.hide()

    def run(self):
        if self.update is not None:
            self.update(self)

    def set_color(self, color):
        self.go.color = color

    def hide(self):
        self.go.visible = False

    def show(self):
        self.go.visible = True


class Button(Element):
    def __init__(self, parent, title="", position=[0,0,0], action=None, update=None, hidden=False):
        super().__init__(parent, object="ui_button", title=title, position=position, update=update, hidden=hidden)
        self.action = action



class ProgressBar(Element):
    def __init__(self, parent, title="", position=[0,0,0], min_scale=[0,0,0], max_scale=[1,1,1], update=None, hidden=False):
        super().__init__(parent, object="ui_bar", title=title, position=position, scale=min_scale, update=update, hidden=hidden)
        self.progress = 0.0
        self.min_scale = min_scale
        self.max_scale = max_scale

    def run(self):
        super().run()

        x = self.min_scale[0] + self.progress * (self.max_scale[0] - self.min_scale[0])
        y = self.min_scale[1] + self.progress * (self.max_scale[1] - self.min_scale[1])
        z = self.min_scale[2] + self.progress * (self.max_scale[2] - self.min_scale[2])
        self.go.worldScale = [x, y, z]


class Label(Element):
    def __init__(self, parent, text="Label", position=[0.0, 0.0, 0.0], size=1.0, update=None, hidden=False):
        super().__init__(parent, object="ui_label", title=text, position=position, update=update, hidden=hidden)
        
        self.text = text
        self.go.size = size
        self.test = 0.0001

    def run(self):
        super().run()

        self.go.text = self.text

        # Approximates font resolution (font.dimensions only available in UPBGE)
        default_px_per_bu = 100
        window_width = render.getWindowWidth()
        view_width = self.go.scene.active_camera.ortho_scale
        pixel_ratio = window_width / view_width # pixels / bu
        self.go.resolution = pixel_ratio / default_px_per_bu


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
        if self.action is not None:
            self.action(self)
