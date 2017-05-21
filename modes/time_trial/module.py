"""
This is the script for the time trial game mode.
It is attached to the Controller object in the mode's blend file.

Checkpoint gD structure:

- time_trial
	- checkpoint_data
		- ID
			- name (obj.name)
			- times {"PLAYER_ID" : [lap0, lap1, lap2, ...]}
			- reference (to bge object)
"""

from bge import logic, events
from modules import level, components, global_constants as G, sound, helpers

from random import randint

import sys
import bgui
import bgui.bge_utils

required_components = ["blocks", "level", "cube", "ship"]

# Queue the required components
queue_id = components.queue(required_components)

sce = logic.getCurrentScene() # scene that contains all objects
gD = logic.globalDict

own = logic.getCurrentController().owner # This is the object that executes these functions.

own["init"] = False

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

		self.lbl_count = bgui.Label(self.frame, text="1", pos=[0.5, 0.8], sub_theme='Large', options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		self.lbl_laps = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.9], options = bgui.BGUI_DEFAULT)
		self.lbl_checkpoints = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.85], options = bgui.BGUI_DEFAULT)
		self.lbl_time = bgui.Label(self.frame, text="Time", pos=[0.5, 0.85], sub_theme='Large', options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)
		self.lbl_time_last_check = bgui.Label(self.frame, text="Time", pos=[0.5, 0.75], options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)

	def update(self):
		if "checkpoint_count_registered" in gD["time_trial"]:
			self.lbl_laps.text = "Lap " + str(gD["time_trial"]["lap"]+1) +"/"+ str(gD["time_trial"]["total_laps"])
			self.lbl_checkpoints.text = "Chk " + str(gD["time_trial"]["checkpoint_count_registered"]) +"/"+ str(gD["time_trial"]["checkpoint_count"])

		


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
			self.lbl_time_last_check.text = helpers.time_string((gD["time_trial"]["checkpoint_data"][last_check]["times"][G.PLAYER_ID][gD["time_trial"]["lap"]]))
		except:
			pass
		if gD["current"]["race_complete"]:
			self.lbl_time.text = self.lbl_time_last_check.text
		else:
			self.lbl_time.text = helpers.time_string(own["Timer"])



def setup():

	# a dict to store all data we need
	gD["time_trial"] = {}
	gD["time_trial"]["checkpoint_data"] = {}

	gD["time_trial"]["lap"] = 0
	gD["time_trial"]["total_laps"] = 3

	# set the music directory
	gD["current"]["music"]["subdir"] = "time_trial"
	gD["current"]["race_complete"] = False

	global ships
	global cp_data
	ships = gD["current"]["ships"] # ship list from global dict
	cp_data = gD["time_trial"]["checkpoint_data"]

	gD["ui"]["sys"].add_overlay(TimeTrialUI)

	# In debug mode, print when game mode is ready
	if G.DEBUG: print(own.name + ": Game mode Time Trial has been set up.")

	own["Timer"] = 0


# The main loop always runs.
def main():

	if not own["init"]:

		# Prepare the game mode by loading the queued components
		components.load()

		# If the queue is emtpy, we're done
		if components.is_done(required_components):
			own["init"] = True
			setup()
	else:
		pass


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
			gD["input"]["focus"] = "ship"
		if own["countdown"] == 0 and own["Timer"] > 5:
			own["countdown"] -= 1


	# check if any ship is near a checkpoint
	for ship in ships:
		ship_ref = ships[ship]["reference"] # the ship object

		for checkpoint in cp_data:
			if ship_ref.getDistanceTo(cp_data[checkpoint]["reference"]) <= TRIGGER_DISTANCE:
				checkpoint_check(ship_ref)
				checkpoint_register(checkpoint, ship_ref)
	if keyboard.events[key_reset] == JUST_RELEASED:
		ship = gD["current"]["ships"][G.PLAYER_ID]["reference"]
		ship.worldPosition = gD["current"]["ships"][G.PLAYER_ID]["last_checkpoint"].worldPosition
		ship.localLinearVelocity = [0, 0, 0]
	if keyboard.events[key_restart] == JUST_RELEASED:
		pass
		# reset all checkpoints and restar the race.

# Use this function with a mesage actuator.
# It gets called whenever the Controller object receives a message.
# In this instance, it is used to refresh the gD when a checkpoint has been activated.
def actions():
	message_sensor = own.sensors["Message"] # This is the sensor that receives messages from other objects, e.g. when a checkpoint has been passed
	if message_sensor.positive and "time_trial.registered" in message_sensor.subjects[-1]:
		if G.DEBUG: print(own.name + ": Message received: "+str(message_sensor.subjects))
		if G.DEBUG: print(own.name + ": Checkpoint passed.")

	# add checkpoints to the gD
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
	if not gD["current"]["race_complete"]:

		time_list = cp_data[checkpoint]["times"]
		ship_id = ship_ref["player_id"]
		lap = gD["time_trial"]["lap"]
		last_checkpoint = gD["current"]["ships"][ship_ref["player_id"]]["last_checkpoint"]

		if not ship_id in time_list:
			time_list[ship_id] = []

		if len(time_list[ship_id])-1 < lap and cp_data[checkpoint]["reference"] != last_checkpoint:
			time_list[ship_id].insert(lap, own["Timer"])
			gD["current"]["ships"][ship_ref["player_id"]]["last_checkpoint"] = cp_data[checkpoint]["reference"]
			sound.play("checkpoint")
			if G.DEBUG: print(str(ship_id), "registered at", checkpoint, "Lap:", lap, "Time:", time_list[ship_id][lap])

# check if a lap has been completed or if the race is over
def checkpoint_check(ship_ref):
	if not gD["current"]["race_complete"]:
		ship_id = ship_ref["player_id"]
		lap = gD["time_trial"]["lap"]
		total_laps = int(gD["time_trial"]["total_laps"])

		amount_registered = 0
		amount_checkpoints = gD["time_trial"]["checkpoint_count"]

		for checkpoint in cp_data:
			time_list = cp_data[checkpoint]["times"]
			if ship_id in time_list:
				if len(time_list[ship_id])-1 == lap:
					amount_registered += 1

		# if len(time_list) >= total_laps:
		gD["time_trial"]["checkpoint_count_registered"] = amount_registered

		if amount_registered == amount_checkpoints:
			amount_registered = 0
			gD["time_trial"]["lap"] += 1
			sound.play("lap_complete")
		# print(gD["time_trial"]["lap"])

		if lap == total_laps:
			gD["input"]["focus"] = "menu"
			if G.DEBUG: print("Time Trial over.")
			sound.play("race_complete")
			gD["time_trial"]["checkpoint_count_registered"] = gD["time_trial"]["checkpoint_count"]
			gD["time_trial"]["lap"] = int(gD["time_trial"]["total_laps"])-1
			gD["current"]["race_complete"] = True
			# components.load("main_menu")



def controls():
	pass
