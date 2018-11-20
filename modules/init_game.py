"""
This is the module called by the controller object in main.blend.
The main function will initialize the globalDict.
"""

from bge import logic
globalDict = logic.globalDict
from modules import ui, menu, game, components, content, config, tests, global_constants as G
import os

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()


def setup():
    if G.DEBUG: os.system('clear')
    print("Brizide ver.", G.VERSION)
    if G.DEBUG: print("D E B U G")

    globalDict["settings"] = config.load() #TODO: remove

    logic.settings = config.load()
    logic.game = game.Game() # new and controlled "global dict"

    logic.components = components.Components() # manages game components loaded by game modes
    logic.game.set_music_dir("menu")

    logic.uim = ui.UIManager()
    logic.uim.set_focus("menu")

    # A dictionary for all the UI layers
    logic.ui = {}

    # get available content
    content.set_all()

    player_dir = os.path.join(G.PATH_PROFILES, logic.settings["Player0"]["Name"])
    if not os.path.isdir(player_dir):
        os.makedirs(player_dir)

    logic.menus = {}

    logic.menus["main_menu"] = menu.Menu(own)

    logic.menus["main_menu"].options.append(
        menu.Option(
            logic.menus["main_menu"], 
            "Start Game", 
            [0, 1, 0], 0)
    )

    logic.menus["main_menu"].options.append(
        menu.Option(
            logic.menus["main_menu"], 
            "Game Mode", 
            [0, 0, 0], 0)
    )

    logic.menus["main_menu"].options.append(
        menu.Option(
            logic.menus["main_menu"], 
            "Level", 
            [0, -1, 0], 0)
    )

def main():
    
    if "main_menu" in logic.menus:
        logic.menus["main_menu"].update()