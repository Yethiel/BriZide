"""
This file contains code for creating and manipulating
a large cube of variable size (track base)
"""

from bge import logic
from modules import helpers


def main():

    """
    A cube size of 10 should result in a driveable area
    of 10x10 tiles per side of the cube.
    """
    sce = helpers.get_scene("Scene")
    own = logic.getCurrentController().owner

    settings = logic.settings
    level = logic.game.get_level()

    # size of the tile objects the cube is made out of (in Blender units)
    tile_size = 32
    cube_size = level.get_cube_size()

    big_cube = sce.addObject("CubeCollision", own, 0)
    big_cube.worldPosition = [(cube_size*tile_size)/2 - 16, (cube_size*tile_size)/2 - 16, (cube_size*tile_size)/2 - 16]
    big_cube.worldScale = [cube_size, cube_size, cube_size]

    if logic.settings["Video"]["simple_cube"] == "True":
        simple_cube = sce.addObject("CubeSimple", own, 0)
        simple_cube.worldPosition = [(cube_size*tile_size)/2 - 16, (cube_size*tile_size)/2 - 16, (cube_size*tile_size)/2 - 16]
        simple_cube.worldScale = [cube_size, cube_size, cube_size]
        logic.components.mark_loaded("cube")
        return


    if cube_size > 0:
        cube_range = range(0, cube_size)

        # create a cube with that size (wall by wall)

        # Z -
        for x in cube_range:
            for y in cube_range:
                own.worldPosition = [x * tile_size,
                                     y * tile_size,
                                     0]

                if logic.settings["Video"]["transparent_tiles"] == "True" and not y % 2:
                    sce.addObject("CubeWindow_Z-", own, 0)
                else:
                    sce.addObject("CubeTile_Z-", own, 0)
        # Z +
        for x in cube_range:
            for y in cube_range:
                own.worldPosition = [x * tile_size,
                                     y * tile_size,
                                     (cube_size-1) * tile_size]

                if logic.settings["Video"]["transparent_tiles"] == "True" and not y % 2:
                    sce.addObject("CubeWindow_Z+", own, 0)
                else:
                    sce.addObject("CubeTile_Z+", own, 0)
        # Y -
        for x in cube_range:
            for z in cube_range:
                own.worldPosition = [x * tile_size,
                                     0,
                                     z * tile_size]

                if logic.settings["Video"]["transparent_tiles"] == "True" and not y % 2:
                    sce.addObject("CubeWindow_Y-", own, 0)
                else:
                    sce.addObject("CubeTile_Y-", own, 0)
        # Y +
        for x in cube_range:
            for z in cube_range:
                own.worldPosition = [x * tile_size,
                                     (cube_size-1) * tile_size,
                                     z * tile_size]

                if logic.settings["Video"]["transparent_tiles"] == "True" and not y % 2:
                    sce.addObject("CubeWindow_Y+", own, 0)
                else:
                    sce.addObject("CubeTile_Y+", own, 0)
        # X -
        for y in cube_range:
            for z in cube_range:
                own.worldPosition = [0,
                                     y * tile_size,
                                     z * tile_size]

                if logic.settings["Video"]["transparent_tiles"] == "True" and not y % 2:
                    sce.addObject("CubeWindow_X-", own, 0)
                else:
                    sce.addObject("CubeTile_X-", own, 0)
        # X +
        for y in cube_range:
            for z in cube_range:
                own.worldPosition = [(cube_size-1) * tile_size,
                                     y * tile_size ,
                                     z * tile_size]

                if logic.settings["Video"]["transparent_tiles"] == "True" and not y % 2:
                    sce.addObject("CubeWindow_X+", own, 0)
                else:
                    sce.addObject("CubeTile_X+", own, 0)

    # tell the components object that loading of this component is done.
    logic.components.mark_loaded("cube")

def clear():
    sce = helpers.get_scene("Scene")

    for obj in sce.objects:
        if "Cube" in obj.name:
            obj.endObject()


