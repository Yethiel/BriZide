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

    # The game object that's used to spawn the UI (addObj)
    logic.uim.go = own

    # Dictionary for the UI layouts
    logic.ui = {}

    # Main menu layout
    layout = logic.ui["layout_main"] = btk.Layout("layout_main", logic.uim.go)
    menu = btk.Menu("menu_main", layout)
    menu.focus()

    # Main menu
    menu.populate(
        texts=[
            "Start Game", 
            "Game Mode", 
            "Level",
            "Quit"
        ], 
        position=[0.5, 5.0, 0],
        size=0.5,
        actions=[
            start_game, 
            show_menu_mode, 
            show_menu_level,
            end_game
        ],
        hidden=False
    )

    # Sub-menu: level selection
    menu_level = btk.Menu("menu_level", layout)
    menu_level.populate(
        texts=logic.game.level_list,
        position=[5.5, 5.0, 0],
        size=0.5,
        actions=[select_level for x in range(len(logic.game.level_list))],
        hidden=True
    )
    menu_level.set_active(logic.game.level_name)

    # Sub-menu: game mode
    menu_mode = btk.Menu("menu_mode", layout)
    menu_mode.populate(
        texts=logic.game.mode_list,
        position=[5.5, 5.0, 0],
        size=0.5,
        actions=[select_mode for x in range(len(logic.game.mode_list))],
        hidden=True
    )
    menu_mode.set_active(logic.game.mode)

    # Misc. menu items
    logo = btk.Element(layout, object="logo", title="logo", position=[0.5, 6, 0], scale=[2,2,1])
    title = btk.Label(layout, text="B r i Z i d e", position=[3, 6.8, 0], size=0.6)
    title.set_color([1, 0.5, 0.0, 1.0])

    # Creates the loading screen
    layout_loading = logic.ui["layout_loading"] = btk.Layout("layout_loading", logic.uim.go)

    # "Loading"
    loading = btk.Label(layout_loading, text="Loading", position=[6.5, 3, 0.2], size=0.6, hidden=True)
    
    # Displays the component that's being loaded
    loading_what = btk.Label(layout_loading, text="", position=[1, 1.15, 0.3], size=0.3, hidden=True, update=update_loading_label)
    loading_what.set_color([0, 0, 0, 1])
    loading_bar = btk.ProgressBar(layout_loading, 
        position=[0, 1, 0.2], 
        hidden=True, 
        min_scale=[0, .5, 1], 
        max_scale=[16, .5, 1],  
        update=update_loading_bar
    )
    
    # Loading screen backdrop
    loading_screen = btk.Element(layout_loading, object="loading_screen", title="loading_screen", position=[0, 0, 0.1], hidden=True)


def update_loading_bar(widget):
    widget.progress = logic.components.get_percent()


def update_loading_label(widget):
    widget.text = logic.components.get_currently_loading()


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
    logic.ui["layout_loading"].show()
    logic.ui["layout_main"].unfocus()
    logic.uim.enqueue("game_start")

def end_game(widget):
    logic.endGame()


def main():
    elements = logic.ui.copy().keys()
    for element in elements:
        if element in logic.ui:
            logic.ui[element].run()