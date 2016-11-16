"""
This is the script for the time trial game mode.
It is attached to the Controller object in the mode's blend file.

Checkpoint globalDict structure:

- current
	- level
		- checkpoint_data
			- ID
				- name (obj.name)
				- times {"PLAYER_ID" : [lap0, lap1, lap2, ...]}
				- reference (to bge object)
"""

from bge import logic, events
from modules import level, components, global_constants as G, sound

from random import randint

import sys
import bgui
import bgui.bge_utils

sce = logic.getCurrentScene() # scene that contains all objects
globalDict = logic.globalDict

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

		self.lbl_velocity = bgui.Label(self.frame, text="velocity", pos=[0.9, 0.1], options = bgui.BGUI_DEFAULT)
		self.lbl_count = bgui.Label(self.frame, text="1", pos=[0.5, 0.8], sub_theme='Large', options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		self.lbl_laps = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.9], options = bgui.BGUI_DEFAULT)
		self.lbl_checkpoints = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.85], options = bgui.BGUI_DEFAULT)

	def update(self):
		if "checkpoint_count_registered" in globalDict["current"]["level"]:
			self.lbl_laps.text = "Lap " + str(globalDict["current"]["level"]["lap"]+1) +"/"+ str(globalDict["current"]["level"]["total_laps"])
			self.lbl_checkpoints.text = "Chk " + str(globalDict["current"]["level"]["checkpoint_count_registered"]) +"/"+ str(globalDict["current"]["level"]["checkpoint_count"])

		if G.PLAYER_ID in globalDict["current"]["ships"]:
			self.lbl_velocity.text = ">>> " + str(int(globalDict["current"]["ships"][G.PLAYER_ID]["reference"]["Velocity"]))


		if own["countdown"] < 4:
			self.lbl_count.text = str(own["countdown"])
		else:
			self.lbl_count.text = ""
		if own["countdown"] == 0:
			self.lbl_count.text = "GO!"
		if own["countdown"] == -1:
			self.lbl_count.text = ""


def setup():

	# load the blocks
	components.load("blocks")

	# load the level
	level.load(globalDict.get("settings")["Game"]["LevelDir"]) # load from file to memory
	components.load("level") # place the level in the 3d world

	# load the cube creator
	components.load("cube")

	# load the ship wrapper
	components.load("ship")

	# countdown



	# set the music directory
	globalDict["current"]["music"]["subdir"] = "time_trial"
	globalDict["current"]["level"]["race_complete"] = False

	global ships
	global cp_data
	ships = globalDict["current"]["ships"] # ship list from global dict
	cp_data = globalDict["current"]["level"]["checkpoint_data"]

	globalDict["ui"]["sys"].add_overlay(TimeTrialUI)

	# In debug mode, print when game mode is ready
	if G.DEBUG: print(own.name + ": Game mode Time Trial has been set up.")

	own["Timer"] = 0


# The main loop always runs.
def main():
	if own["countdown"] > -1 and own["Timer"] > 1:
		if own["countdown"] == 4:
			sound.play("three" + str(randint(0,4)))
			# sound.EchoWrapper("three0").play()
			own["countdown"] -= 1
		if own["countdown"] == 3 and own["Timer"] > 2:
			sound.play("two" + str(randint(0,4)))
			own["countdown"] -= 1
		if own["countdown"] == 2 and own["Timer"] > 3:
			sound.play("one" + str(randint(0,4)))
			own["countdown"] -= 1
		if own["countdown"] == 1 and own["Timer"] > 4:
			# sound.play("go" + str(randint(0,4)))
			sound.EchoWrapper("go" + str(randint(0,4))).play()
			own["countdown"] -= 1
			# Give controls to the player
			globalDict["input"]["focus"] = "ship"
		if own["countdown"] == 0 and own["Timer"] > 5:
			own["countdown"] -= 1


	# check if any ship is near a checkpoint
	for ship in ships:
		ship_ref = ships[ship]["reference"] # the ship object

		for checkpoint in cp_data:
			if ship_ref.getDistanceTo(cp_data[checkpoint]["reference"]) <= TRIGGER_DISTANCE:
				# send a message with the subject "activate" with the body of the ship's name (to the checkpoint, from the ship)
				checkpoint_check(ship_ref)
				checkpoint_register(checkpoint, ship_ref)
	if keyboard.events[key_reset] == JUST_RELEASED:
		ship = globalDict["current"]["ships"][G.PLAYER_ID]["reference"]
		ship.worldPosition = globalDict["current"]["ships"][G.PLAYER_ID]["last_checkpoint"].worldPosition
		ship.localLinearVelocity = [0, 0, 0]
	if keyboard.events[key_restart] == JUST_RELEASED:
		pass
		# reset all checkpoints and restar the race.

# Use this function with a mesage actuator.
# It gets called whenever the Controller object receives a message.
# In this instance, it is used to refresh the globalDict when a checkpoint has been activated.
def actions():
	message_sensor = own.sensors["Message"] # This is the sensor that receives messages from other objects, e.g. when a checkpoint has been passed
	if message_sensor.positive and "time_trial.registered" in message_sensor.subjects[-1]:
		if G.DEBUG: print(own.name + ": Message received: "+str(message_sensor.subjects))
		if G.DEBUG: print(own.name + ": Checkpoint passed.")

	# add checkpoints to the globalDict
	if message_sensor.positive:
		for msg in range(0, len(message_sensor.subjects)): # messages can arrive at the same time. work on all of them
			if "checkpoint.setup" in message_sensor.subjects[msg]:
				for obj in sce.objects:
					if "id" in obj and message_sensor.bodies[msg] in str(obj["id"]):

						# setup entry in the global current level dict (checkpoint_data)
						cp_data[int(obj["id"])] = {
							"name": obj.name,
							"times" : {}, # ship : [laptime1, laptime2, ...]
							"reference" : obj # a reference to the object itself used in ship.near
						}
						if G.DEBUG: print(own.name + ": Set up checkpoint: "+str(obj["id"]))

### Other Functions

# When a ship passes a checkpoint, register it
def checkpoint_register(checkpoint, ship_ref):
	if not globalDict["current"]["level"]["race_complete"]:

		time_list = cp_data[checkpoint]["times"]
		ship_id = ship_ref["player_id"]
		lap = globalDict["current"]["level"]["lap"]
		last_checkpoint = globalDict["current"]["ships"][ship_ref["player_id"]]["last_checkpoint"]

		if not ship_id in time_list:
			time_list[ship_id] = []

		if len(time_list[ship_id])-1 < lap and cp_data[checkpoint]["reference"] != last_checkpoint:
			time_list[ship_id].insert(lap, own["Timer"])
			globalDict["current"]["ships"][ship_ref["player_id"]]["last_checkpoint"] = cp_data[checkpoint]["reference"]
			sound.play("checkpoint")
			if G.DEBUG: print(str(ship_id), "registered at", checkpoint, "Lap:", lap, "Time:", time_list[ship_id][lap])

# check if a lap has been completed or if the race is over
def checkpoint_check(ship_ref):
	if not globalDict["current"]["level"]["race_complete"]:
		ship_id = ship_ref["player_id"]
		lap = globalDict["current"]["level"]["lap"]
		total_laps = int(globalDict["current"]["level"]["total_laps"])

		amount_registered = 0
		amount_checkpoints = globalDict["current"]["level"]["checkpoint_count"]

		for checkpoint in cp_data:
			time_list = cp_data[checkpoint]["times"]
			if ship_id in time_list:
				if len(time_list[ship_id])-1 == lap:
					amount_registered += 1

		# if len(time_list) >= total_laps:
		globalDict["current"]["level"]["checkpoint_count_registered"] = amount_registered

		if amount_registered == amount_checkpoints:
			amount_registered = 0
			globalDict["current"]["level"]["lap"] += 1
			sound.play("lap_complete")
		# print(globalDict["current"]["level"]["lap"])

		if lap == total_laps:
			globalDict["input"]["focus"] = "menu"
			if G.DEBUG: print("Time Trial over.")
			sound.play("race_complete")
			globalDict["current"]["level"]["checkpoint_count_registered"] = globalDict["current"]["level"]["checkpoint_count"]
			globalDict["current"]["level"]["lap"] = int(globalDict["current"]["level"]["total_laps"])-1
			globalDict["current"]["level"]["race_complete"] = True
			# components.load("main_menu")



def controls():
	pass
