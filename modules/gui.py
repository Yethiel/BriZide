from bge import logic
from modules import btk

from modules import global_constants as G

class UIManager():
    def __init__(self):

        self.focus = "menu"
        self.queue = []
        self.go = None  # Game object used to spawn ui elements

    def set_focus(self, element):
        if G.DEBUG: print("Set focus to", element)
        self.focus = element

    def enqueue(self, command):
        self.queue.append(command)


def setup():

    own = logic.getCurrentController().owner

    logic.uim.go = own

    logic.ui = {}

    layout = logic.ui["layout_main"] = btk.Layout("layout_main", logic.uim.go)
    menu = btk.Menu("menu_main", layout)
    menu.focus()

    menu.populate(
        texts=[
            "Start Game", 
            "Game Mode", 
            "Level"
        ], 
        position=[0.5, 5.0, 0],
        size=0.5,
        actions=[
            start_game, 
            show_menu_mode, 
            show_menu_level
        ],
        hidden=False
    )

    menu_level = btk.Menu("menu_level", layout)
    menu_level.populate(
        texts=logic.game.level_list, 
        position=[5.5, 5.0, 0],
        size=0.5,
        actions=[select_level for x in range(len(logic.game.level_list))],
        hidden=True
    )
    menu_level.set_active(logic.game.level_name)


    menu_mode = btk.Menu("menu_mode", layout)
    menu_mode.populate(
        texts=logic.game.mode_list, 
        position=[5.5, 5.0, 0],
        size=0.5,
        actions=[select_mode for x in range(len(logic.game.mode_list))],
        hidden=True
    )
    menu_mode.set_active(logic.game.mode)

    logo = btk.Element(layout, "logo", [0.5, 6, 0])
    title = btk.Label(layout, text="B r i Z i d e", position=[3, 6.8, 0], size=0.6)
    title.set_color([1, 0.5, 0.0, 1.0])


def show_menu_level(widget):
    logic.ui["layout_main"].get_element("menu_level").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_level").focus()


def show_menu_mode(widget):
    logic.ui["layout_main"].get_element("menu_mode").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_mode").focus()


def select_level(widget):
    logic.game.set_level(widget.text)
    logic.ui["layout_main"].get_element("menu_level").unfocus()
    logic.ui["layout_main"].get_element("menu_main").focus()
    logic.ui["layout_main"].get_element("menu_level").hide()


def select_mode(widget):
    logic.game.set_mode(widget.text)
    logic.ui["layout_main"].get_element("menu_mode").unfocus()
    logic.ui["layout_main"].get_element("menu_main").focus()
    logic.ui["layout_main"].get_element("menu_mode").hide()


def start_game(widget):
    logic.ui["layout_main"].hide()
    logic.ui["layout_main"].unfocus()
    logic.uim.enqueue("game_start")


def main():
    elements = logic.ui.copy().keys()
    for element in elements:
        if element in logic.ui:
            logic.ui[element].run()