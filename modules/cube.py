"""
This file contains code for creating and manipulating
a large cube of variable size (track base)
"""

from bge import logic

co = logic.getCurrentController()
own = co.owner
sce = logic.getCurrentScene()

settings = logic.globalDict.get("settings")
level = logic.game.get_level()
tile_size = 32
cube_size = level.get_cube_size()

def main():
	# get cube size from settings
	"""
	defining how many cubes have to be placed. + 2 since two blocks will be used for the walls
	(we're counting tiles that you can drive on for the cube size).
	A cube size of 10 should result in a driveable area of 10x10 tiles per side of the cube.
	"""
	if cube_size > 0:
		cube_range = range(0, cube_size)

		# create a cube with that size (wall by wall)

		# Z -
		for x in cube_range:
			for y in cube_range:
				own.worldPosition = [x * tile_size, y * tile_size, 0]
				sce.addObject("CubeTile_Z-", own, 0)
		# Z +
		for x in cube_range:
			for y in cube_range:
				own.worldPosition = [x * tile_size, y * tile_size, (cube_size-1) * tile_size]
				sce.addObject("CubeTile_Z+", own, 0)
		# Y -
		for x in cube_range:
			for z in cube_range:
				own.worldPosition = [x * tile_size, 0, z * tile_size]
				sce.addObject("CubeTile_Y-", own, 0)
		# Y +
		for x in cube_range:
			for z in cube_range:
				own.worldPosition = [x * tile_size, (cube_size-1) * tile_size, z * tile_size]
				sce.addObject("CubeTile_Y+", own, 0)
		# X -
		for y in cube_range:
			for z in cube_range:
				own.worldPosition = [0, y * tile_size, z * tile_size]
				sce.addObject("CubeTile_X-", own, 0)
		# X +
		for y in cube_range:
			for z in cube_range:
				own.worldPosition = [(cube_size-1) * tile_size, y * tile_size , z * tile_size]
				sce.addObject("CubeTile_X+", own, 0)

	logic.components.mark_loaded("cube")
