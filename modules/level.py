"""
This module is for managing levels.
Objects from the classes defined here will be saved in the globalDict.
"""

import os
import pickle
import configparser
import mathutils
from bge import logic
from modules import global_constants as G

co = logic.getCurrentController()
sce = logic.getCurrentScene()
own = co.owner
settings = logic.globalDict.get("settings")

class Block():
	def __init__(self):
		self.

class Level():
	"""Used for loading and storing level data

	A level does not include anything related to the game modes.
	There is no information about laps or checkpoints.
	This is solely to set up the game world.

	Attributes:
		identifier: A string that represents the level, e.g. folder name
		path: Path to the level folder
		cube_size: Size of the cube that encloses the level
		start_pos: Coordinate of the start position (x, y, z)
		start_orientation: Orientation for the spawn position
		__block_data: List of block objects that the level includes
		__valid: True if everything loaded correctly
		inf_path: path + .inf file name
		blk_path: path + .blk file name

	"""
	def __init__(self, identifier):
		"""Init level objet with defaults"""
		self.identifier = identifier
		self.path = G.PATH_LEVELS + self.identifier
		self.cube_size = 32
		self.start_pos = [0, 0, 0]
		self.start_orientation = []
		self.__block_data =[]
		self.__valid = True

		self.__lap = 0
		self.__total_laps = 0

		self.inf_path = self.path + self.identifier + G.EXTENSION_INF
		self.blk_path = self.path + self.identifier + G.EXTENSION_BLK

	def __str__(self):
		"""String representation"""
		return self.identifier

	def print_info(self):
		"""Print debug information, mainly attributes"""
		print("=== LEVEL INFORMATION ===")
		print("\tName: {}".format(self.identifier))
		print("\tCube Size: {}".format(self.cube_size))
		print("\tStart Pos: {}".format(self.start_pos))
		print("\tStart Orientation: {}".format(self.start_orientation))
		print("\tNumber of Blocks: {}".format(len(self.__blocks)))

	def get_checkpoint_count(self):
		"""The checkpoint count will only be set by load(), thus only get"""
		return self.__checkpoint_count
 
	def load(self):
		"""Load the level from its folder"""
		
		# Load the information file
		if os.path.isfile(self.inf_path):
			inf_file = configparser.ConfigParser()
			inf_file.read(self.inf_path)
			if G.DEBUG: print("{}: {}".format(own.name, 
				"Loaded level information file.")
		else:
			if G.DEBUG: print("{}: {}".format(own.name, 
				"Could not load level information file.")
			self.__valid = False
			return 0

		# Load the block file
		if os.path.isfile(blk_path):
			blk_file = pickle.load(open(self.blk_path, "rb"))
		else:
			print("{}: {}".format(own.name, "No .blk file found.")
			self.__valid = False
			return 0

		for block in blk_file["blocks"]:
			# Get start position from start object
			if "Start" in block["type"]:
				self.start_pos = block["position"]
				self.start_orientation = block["orientation"]
			
		# Set attributes
		self.cube_size = inf["meta"]["cube_size"])
			
		# Make this object accessible in the globalDict
		logic.globalDict["current"]["level"] = self

def save():
	settings = logic.globalDict.get("settings")
	level_dict = logic.globalDict.get("current")["level"]
	level_path = logic.expandPath("//levels/"+level_dict["name"])
	inf_path = logic.expandPath("//levels/"+level_dict["name"]+"/"+level_dict["name"]+".inf")
	blk_path = logic.expandPath("//levels/"+level_dict["name"]+"/"+level_dict["name"]+".blk")

	# prepare block dict
	blocks = []
	checkpoint_count = 0
	portal_count = 0

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

			elif "Portal" in obj.name:
				if not "id" in obj:
					block["id"] = portal_count
					if block["id"] == 0:
						block["link_id"] = 1
					else: 
						block["link_id"] = 0
				portal_count += 1

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
		
		if "link_id" in block:
			nb["link_id"] = block["link_id"]
		
		nb.worldPosition = block["position"]
		do = nb.worldOrientation.to_euler()
		
		for x in [0, 1, 2]:
			do[x] = block["orientation"][x]
		
		nb.worldOrientation = do.to_matrix()
		logic.NextFrame()