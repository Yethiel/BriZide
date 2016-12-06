"""
This is the script for the time trial game mode.
It is attached to the Controller object in the mode's blend file.

Checkpoint gD structure:

- current
	- level
		- checkpoint_data
			- ID
				- name (obj.name)
				- times {"PLAYER_ID" : [lap0, lap1, lap2, ...]}
				- reference (to bge object)
"""

from bge import logic, events
from modules import components, global_constants as G, sound, helpers

from random import randint

import sys
import bgui
import bgui.bge_utils

sce = logic.getCurrentScene() # scene that contains all objects
gD = logic.globalDict

own = logic.getCurrentController().owner # This is the object that executes these functions.

TRIGGER_DISTANCE = 32 # distance for a checkpoint to be triggered

own["countdown"] = 4

own["init_cp"] = False #whether the checkpoints have been set up


# Setup is executed as soon as the game mode has been loaded.

keyboard = logic.keyboard
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

#Key assignments Keyboard, will be loaded from settings
key_reset = events.BACKSPACEKEY
key_restart = events.DELKEY
# key_menu_confirm = events.ENTERKEY

class TimeTrialUI(bgui.bge_utils.Layout):
	def __init__(self, sys, data):
		super().__init__(sys, data)
		self.frame = bgui.Frame(self, border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

		self.lbl_velocity = bgui.Label(
			self.frame,
			text="velocity", 
			pos=[0.9, 0.1], 
			options = bgui.BGUI_DEFAULT)

		self.lbl_count = bgui.Label(self.frame, text="1", pos=[0.5, 0.8], sub_theme='Large', options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		self.lbl_laps = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.9], options = bgui.BGUI_DEFAULT)
		self.lbl_checkpoints = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.85], options = bgui.BGUI_DEFAULT)
		self.lbl_time = bgui.Label(self.frame, text="Time", pos=[0.5, 0.85], sub_theme='Large', options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)
		self.lbl_time_last_check = bgui.Label(self.frame, text="Time", pos=[0.5, 0.75], options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)

	def update(self):
		if "checkpoint_count_registered" in gD["current"]["level"]:
			self.lbl_laps.text = "Lap " + str(gD["current"]["level"]["lap"]+1) +"/"+ str(gD["current"]["level"]["total_laps"])
			self.lbl_checkpoints.text = "Chk " + str(gD["current"]["level"]["checkpoint_count_registered"]) +"/"+ str(gD["current"]["level"]["checkpoint_count"])

		if G.PLAYER_ID in gD["current"]["ships"]:
			self.lbl_velocity.text = ">>> " + str(int(gD["current"]["ships"][G.PLAYER_ID]["reference"]["Velocity"]))


		if own["countdown"] < 4:
			self.lbl_count.text = str(own["countdown"])
		else:
			self.lbl_count.text = ""
		if own["countdown"] == 0:
			self.lbl_count.text = "GO!"
		if own["countdown"] == -1:
			self.lbl_count.text = ""


		try:
			last_check = gD["current"]["ships"][G.PLAYER_ID]["last_checkpoint"]["id"]
			self.lbl_time_last_check.text = helpers.time_string((gD["current"]["level"]["checkpoint_data"][last_check]["times"][G.PLAYER_ID][gD["current"]["level"]["lap"]]))
		except:
			pass
		if gD["current"]["level"]["race_complete"]:
			self.lbl_time.text = self.lbl_time_last_check.text
		else:
			self.lbl_time.text = helpers.time_string(own["Timer"])



def setup():

	# load the blocks
	components.load("blocks")

	# load the level
	components.load("level") # place the level in the 3d world

	# load the cube creator
	components.load("cube")

	# load the ship wrapper
	components.load("ship")

	# set the music directory
	# gD["current"]["music"]["subdir"] = "free"
	# gD["current"]["level"]["race_complete"] = False

	global ships
	global cp_data
	ships = gD["current"]["ships"] # ship list from global dict

	# gD["ui"]["sys"].add_overlay(TimeTrialUI)

	# In debug mode, print when game mode is ready
	if G.DEBUG: print(own.name + ": Game mode Free has been set up.")

	own["Timer"] = 0
	gD["input"]["focus"] = "ship"


# The main loop always runs.
def main():

	pass


def controls():
	pass
