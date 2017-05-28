"""
This is the module called by the controller object in main.blend.
The main function will initialize the globalDict.
"""

from bge import logic
globalDict = logic.globalDict
from modules import game, components, content, modes, config, global_constants as G
import os

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()


def setup():
	os.system('clear')
	print("Brizide ver.", G.VERSION)
	if G.DEBUG: print("D E B U G")
	globalDict["settings"] = config.load()
	logic.game = game.Game() # new controlled "global dict"

	### Preparing the globalDict

	# contains properties for the current game session (levels, selected ship, start position, etc.)
	current_game = {
		"level" : None,			# the level to be loaded in any game mode
		"ships" : {},			# list of ships/players. a dict with {ship_id : {}, ...}
		"block_list" : [],
		"music" : {
			"subdir" : "menu",
			"play" : True
		}
	}

	globalDict["input"] = {		# this is for control modules to check whether they are in focus
		"focus" : "menu"
	}
	globalDict["current"] = current_game

	globalDict["ui"] = {}

	# get available content
	content.set_all()

def main():
	pass

def end_menu():
	for scene in logic.getSceneList():
		if "UI_Menu" in scene.name:
			scene.end()
	components.free("main_menu")


# actions are triggered with a message sensor. messages are sent by the UI
def actions():
	message_sensor = own.sensors["msg"]

	# this starts the game with the selected mode and settings
	if message_sensor.positive and "start" in str(message_sensor.subjects):
		mode = str(message_sensor.bodies[0])
		components.load_immediate("../modes/" + mode + "/" + mode)
		end_menu()

