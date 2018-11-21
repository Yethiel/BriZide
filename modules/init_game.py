"""
This is the module called by the controller object in main.blend.
The main function will initialize the globalDict.
"""

from bge import logic
from modules import gui, game, components, content, config, tests, global_constants as G
import os

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()


def setup():
    if G.DEBUG: os.system('clear')
    print("Brizide ver.", G.VERSION)
    if G.DEBUG: print("D E B U G")

    logic.settings = config.load()
    logic.game = game.Game() # new and controlled "global dict"

    logic.components = components.Components() # manages game components loaded by game modes
    logic.game.set_music_dir("menu")

    logic.uim = gui.UIManager()
    logic.uim.set_focus("menu")

    # get available content
    content.set_all()

    player_dir = os.path.join(G.PATH_PROFILES, logic.settings["Player0"]["Name"])
    if not os.path.isdir(player_dir):
        os.makedirs(player_dir)

    logic.addScene("Menu")
    logic.addScene("Skybox", 0)
    logic.uim.set_focus("menu")



def main():
    
    if logic.uim.queue:
        if logic.uim.queue[0] == "game_start":
            logic.game.start()
            logic.uim.queue.pop(0)