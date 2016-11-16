"""
These functions will go through the folders and search for (user) content.
set_all() will set the entry in the globalDict
Mainly used for frontend to load with components.py or modes.py.

TL;DR: Get name lists of available content
"""
from bge import logic
from os import listdir

def get_levels():
	levels = []
	for folder in listdir(logic.expandPath("//levels/")):
		if folder+".inf" in listdir(logic.expandPath("//levels/"+folder)):
			levels.append(folder)
	return levels

def get_ships():
	ships = []
	for folder in listdir(logic.expandPath("//ships/")):
		if folder+".inf" in listdir(logic.expandPath("//ships/"+folder)):
			ships.append(folder)
	return ships

def get_modes():
	modes = []
	for folder in listdir(logic.expandPath("//modes/")):
		if folder+".inf" in listdir(logic.expandPath("//modes/"+folder)):
			modes.append(folder)
	return modes

def set_all():
	logic.globalDict["content"] = {
		"levels" : get_levels(),
		"modes" : get_modes(),
		"ships" : get_ships()
		}
