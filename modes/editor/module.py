"""
This is the script for the E D I T O R.
Be careful with this. If you change too many things, others might not be able to open your tracks.
It is attached to the Controller object in the mode's blend file.
"""

from bge import logic
from modules import level, components, global_constants as G
from modules.ui_editor import EditorUI

globalDict = logic.globalDict
own = logic.getCurrentController().owner # This is the object that executes these functions.

# Setup is executed as soon as the game mode has been loaded.
def setup():
	### Prepare the global dict
	editor = {
		"selected_block" : "Block_0_32_32_32" # yay defaults
	}
	globalDict["editor"] = editor

	# load the blocklib to get add all available blocks to the global directions
	# this component will always free itself since its only purpose is to
	# generate a list of blocks it contains
	components.load("blocklib")

	# load the block component
	components.load("blocks")

	# finally, load the editor and all its user friendly stuff
	components.load("editor")

	# load the level
	level.load(globalDict.get("settings")["Game"]["LevelDir"])
	components.load("level")

	# load the cube creator
	components.load("cube")

	# the blocklib will free itself after main() is done.
	# logic.addScene("UI_Editor")

	# unlock ship
	globalDict["input"]["focus"] = "editor_main"

	# set the music directory
	globalDict["current"]["music"]["subdir"] = "editor"

	globalDict["ui"]["sys"].add_overlay(EditorUI)

	print(own.name + ": Editor has been set up.")

# The main loop always runs.
def main():
	pass

# Use this function with a mesage actuator.
# It gets called whenever the Controller object receives a message.
# In this instance, it is used to refresh the globalDict when a checkpoint has been activated.
def actions():
	print(own.name + ": Message received.")
