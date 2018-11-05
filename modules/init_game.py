"""
This is the module called by the controller object in main.blend.
The main function will initialize the globalDict.
"""

from bge import logic
globalDict = logic.globalDict
from modules import game, components, content, modes, config, tests, global_constants as G
import os

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()


def setup():
    if G.DEBUG: os.system('clear')
    print("Brizide ver.", G.VERSION)
    if G.DEBUG: print("D E B U G")

    globalDict["settings"] = config.load()
    logic.game = game.Game() # new and controlled "global dict"
    print(logic.game.mode)
    logic.components = components.Components() # manages game components loaded by game modes
    logic.game.set_music_dir("menu")

    globalDict["input"] = {     # this is for control modules to check whether they are in focus
        "focus" : "menu"
    }

    # A dictionary for all the UI layers
    logic.ui = {}

    # get available content
    content.set_all()

    player_dir = os.path.join(G.PATH_PROFILES, globalDict["settings"]["Game"]["name"])
    if not os.path.isdir(player_dir):
        os.makedirs(player_dir)

def main():
    pass
    # tests.main()

# def end_menu():
#     """Deprecated"""
#     for scene in logic.getSceneList():
#         if "UI_Menu" in scene.name:
#             scene.end()
#     components.free("main_menu")


# actions are triggered with a message sensor. messages are sent by the UI
def actions():
    pass
    # message_sensor = own.sensors["msg"]

    # # this starts the game with the selected mode and settings
    # if message_sensor.positive and "start" in str(message_sensor.subjects):
    #   mode = str(message_sensor.bodies[0])
    #   components.load_immediate("../modes/" + mode + "/" + mode)
    #   end_menu()
