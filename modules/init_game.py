"""
This is the module called by the controller object in main.blend.
"""

from bge import logic, events, render
from modules import sound, gui, game, components, content, config, video, sound, global_constants as G
import os, sys, datetime

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()

kbd = logic.keyboard
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

def setup():
    print("Brizide ver.", G.VERSION)

    logic.settings = config.load()
    G.DEBUG = logic.settings["Dev"]["debug"] == "True"
    video.apply_settings()
    if G.DEBUG: 
        os.system('clear')
        print("D E B U G")
        render.showProfile(True)
        render.showProperties(True)
        render.showFramerate(True)
    sound.init()
    logic.game = game.Game(own)

    logic.components = components.Components() # manages game components loaded by game modes
    logic.game.set_music_dir("menu")

    logic.uim = gui.UIManager()
    logic.uim.set_focus("menu")

    # gets available content
    content.set_all()

    player_dir = os.path.join(G.PATH_PROFILES, logic.settings["Player"]["Name"])
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

    if kbd.events[events.F8KEY] == JUST_RELEASED:
        sound.play("race_complete")
        render.makeScreenshot(logic.expandPath("//screenshots/brizide-{date:%Y-%m-%d %H:%M:%S}".format( date=datetime.datetime.now() )))
