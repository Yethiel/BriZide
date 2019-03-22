"""
This is the module called by the controller object in main.blend.
"""

from bge import logic
from modules import sound, gui, game, components, content, config, video, global_constants as G
import os, sys

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()


def setup():
    print("Brizide ver.", G.VERSION)

    logic.settings = config.load()
    G.DEBUG = logic.settings["Dev"]["debug"] == "True"
    video.apply_settings()
    if G.DEBUG: print("D E B U G")
    if G.DEBUG: os.system('clear')
    sound.init()
    logic.game = game.Game(own)

    logic.components = components.Components() # manages game components loaded by game modes
    logic.game.set_music_dir("menu")

    logic.uim = gui.UIManager()
    logic.uim.set_focus("menu")

    # gets available content
    content.set_all()

    player_dir = os.path.join(G.PATH_PROFILES, logic.settings["Player0"]["Name"])
    if not os.path.isdir(player_dir):
        os.makedirs(player_dir)

    logic.addScene("Menu")
    logic.addScene("Skybox", 0)
    logic.uim.set_focus("menu")


def main():
    """
    Workaround: Starting the game from the context of a different
        scene other than the main one breaks the component system.
        So the UI puts a command in the queue which then gets
        executed here.
    """
    if logic.uim.queue:
        if logic.uim.queue[0] == "game_start":
            logic.game.start()
            logic.uim.queue.pop(0)
