"""
This script contains all functions that can be
perfomed on or with levels (files and instances in the game)
"""

from bge import logic
import pickle
import configparser
import os
import mathutils
from scripts import global_constants as G

co = logic.getCurrentController()
sce = logic.getCurrentScene()
own = co.owner


def load(level_name):

	settings = logic.globalDict.get("settings")
	level_path = logic.expandPath("//levels/"+level_name)
	inf_path = logic.expandPath("//levels/"+level_name+"/"+level_name+".inf")
	blk_path = logic.expandPath("//levels/"+level_name+"/"+level_name+".blk")

	# load the information file
	inf = configparser.ConfigParser()
	if os.path.isfile(inf_path):
		inf.read(inf_path)
		if G.DEBUG: print("Loaded level information file.")

	# load the block file
	start_pos = [0, 0, 0]
	start_orientation = []
	checkpoint_count = 0
	blk_file = {
		"blocks" : []
	}

	if os.path.isfile(blk_path):
		blk_file = pickle.load( open( blk_path, "rb" ) )
	else:
		print("No .blk file found.")
	for block in blk_file["blocks"]:
		# get start position from start object
		if "Start" in block["type"]:
			start_pos = block["position"]
			start_orientation = block["orientation"]
		# get checkpoint_count
		elif "Checkpoint" in block["type"]:
			block["id"] = checkpoint_count # set an id for the checkpoint
			checkpoint_count += 1

	level_dict = {
		"name" : inf["info"]["name"],
		"lap" : 0,
		"total_laps": settings["Game"]["laps"],
		"cube_size" : int(inf["meta"]["cube_size"]),
		"block_list" : blk_file["blocks"],
		"start_pos" : start_pos,
		"start_orientation" : start_orientation,
		"checkpoint_count" : checkpoint_count,
		"checkpoint_data" : {}
	}
	if G.DEBUG:
		print("=== LEVEL INFORMATION ===")
		print("    Name: "+ str(level_dict["name"]))
		print("    Cube Size: "+ str(level_dict["cube_size"]))
		print("    Start Pos: "+ str(level_dict["start_pos"]))
		print("    Start Orientation: "+ str(level_dict["start_orientation"]))
		print("    Number of Blocks: "+ str(len(level_dict["block_list"])))
		print("    Checkpoints: "+ str(level_dict["checkpoint_count"]))

	logic.globalDict["current"]["level"] = level_dict

def save():
	settings = logic.globalDict.get("settings")
	level_dict = logic.globalDict.get("current")["level"]
	level_path = logic.expandPath("//levels/"+level_dict["name"])
	inf_path = logic.expandPath("//levels/"+level_dict["name"]+"/"+level_dict["name"]+".inf")
	blk_path = logic.expandPath("//levels/"+level_dict["name"]+"/"+level_dict["name"]+".blk")

	# prepare block dict
	blocks = []
	checkpoint_count = 0

	# Save all saveable blocks
	for obj in sce.objects:
		if "Block_" in obj.name:
			wo = obj.worldOrientation.to_euler() # saving the start orientation as an euler matrix (saves some digits)

			block = {
				"type" : obj.meshes[0].name,
				"position" : [obj.worldPosition.x, obj.worldPosition.y, obj.worldPosition.z],
				"orientation" : [wo[0], wo[1], wo[2]]
			}
			if "Checkpoint" in obj.name:
				if not "id" in obj:
					block["id"] = checkpoint_count
				else:
					block["id"] = obj["id"]
				checkpoint_count += 1

			blocks.append(block)

	blk_file = {
		"version" : settings["Game"]["Version"],
		"author" : settings["Game"]["Name"],
		"blocks" : blocks,
		"checkpoint_count" : checkpoint_count
	}
	pickle.dump( blk_file, open( blk_path, "wb" ) )
	print("Saved block file.")

	# write .inf file
	inf = configparser.ConfigParser()
	inf["info"] = {
		"name" : level_dict["name"]
	}
	inf["meta"] = {
		"cube_size" : level_dict["cube_size"]
	}


	with open(inf_path, 'w') as inffile:
		inf.write(inffile)
	print("Saved information file.")


def place():
	# assuming that the level itself has been loaded in to the global dict, we can now actually load it into the 3d world.
	level_dict = logic.globalDict.get("current")["level"]
	for block in level_dict["block_list"]:

		nb = sce.addObject(block["type"])
		if "id" in block:
			nb["id"] = block["id"]
		nb.worldPosition = block["position"]
		do = nb.worldOrientation.to_euler()
		for x in [0, 1, 2]:
			do[x] = block["orientation"][x]
		nb.worldOrientation = do.to_matrix()
		logic.NextFrame()
		# for a in range(0, 2):
		#     for b in range(0, 2):
		#         nb.worldOrientation[a][b] = block["orientation"][a][b]
