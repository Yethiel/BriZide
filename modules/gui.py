from bge import logic
from modules import btk


class UIManager():
    def __init__(self):

        self.focus = "menu"
        self.queue = []
        self.go = None  # Game object used to spawn ui elements

    def set_focus(self, element):
        self.focus = element

    def enqueue(self, command):
        self.queue.append(command)


def setup():

    own = logic.getCurrentController().owner

    logic.uim.go = own

    logic.ui = {}

    logic.ui["main_menu"] = btk.Menu(own)
    logic.ui["main_menu"].focus()
    logic.ui["main_menu"].populate(
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

    logic.ui["main_menu_level"] = btk.Menu(own)
    logic.ui["main_menu_level"].populate(
        texts=logic.game.level_list, 
        position=[5.5, 5.0, 0],
        size=0.5,
        actions=[select_level for x in range(len(logic.game.level_list))],
        hidden=True
    )
    logic.ui["main_menu_level"].set_active(logic.game.level_name)


    logic.ui["main_menu_mode"] = btk.Menu(own)
    logic.ui["main_menu_mode"].populate(
        texts=logic.game.mode_list, 
        position=[5.5, 5.0, 0],
        size=0.5,
        actions=[select_mode for x in range(len(logic.game.mode_list))],
        hidden=True
    )
    logic.ui["main_menu_mode"].set_active(logic.game.mode)


def show_menu_level(widget):
    logic.ui["main_menu_level"].show()
    logic.ui["main_menu"].unfocus()
    logic.ui["main_menu_level"].focus()


def show_menu_mode(widget):
    logic.ui["main_menu_mode"].show()
    logic.ui["main_menu"].unfocus()
    logic.ui["main_menu_mode"].focus()


def select_level(widget):
    logic.game.set_level(widget.text)
    logic.ui["main_menu_level"].unfocus()
    logic.ui["main_menu"].focus()
    logic.ui["main_menu_level"].hide()


def select_mode(widget):
    logic.game.set_mode(widget.text)
    logic.ui["main_menu_mode"].unfocus()
    logic.ui["main_menu"].focus()
    logic.ui["main_menu_mode"].hide()


def start_game(widget):
    logic.ui["main_menu"].hide()
    logic.uim.enqueue("game_start")


def main():
    for m in logic.ui:
        logic.ui[m].run()