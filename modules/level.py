"""
This module is for managing levels.
Objects from the classes defined here will be saved in the gD.
"""

import os
import json
import mathutils
from bge import logic
from modules import helpers, global_constants as G

class Block():
    """Used for storing block data from the level files

    These objets will be in the block_data list of the Level-class objects

    Attributes:
        type: Block type name as a string
        position: BGE worldPosition
        orientation: BGE worldOrientation
        id: Unique ID of the block
        properties: A dictionary of BGE properties (e.g. portal links, effects)
    """
    def __init__(
        self, type=None, position=None, orientation=None, id=None,
        properties=None):

        if type is None:
            self.type = "Default"
        else:
            self.type = type

        if position is None:
            self.position = [0, 0, 0]
        else:
            self.position = position

        if orientation is None:
            self.orientation = [[], [], []]
        else:
            self.orientation = orientation

        if id is None:
            self.id = -1
        else:
            self.id = -1

        if properties is None:
            self.properties = {}
        else:
            self.properties = properties

    def __str__(self):
        return "{} {}".format(type, id)


class Level():
    # TODO(Yethiel): Rework the start pos and orientation: RV-like Grid layout
    """Used for loading and storing level data

    A level does not include anything related to the game modes.
    There is no information about laps or checkpoints.
    This is solely to set up the game world.

    After the level has been placed, changes to the objects of this class
    will not do anything. All actions happen in the 3D world.
    Dynamic variables (laps, checkpoints, ...) depend on the game mode.

    Attributes:
        identifier: A string that represents the level, e.g. folder name
        path: Path to the level folder
        cube_size: Size of the cube that encloses the level
        start_pos: Coordinate of the start position (x, y, z)
        start_orientation: Orientation for the spawn position
        block_data: List of block objects that the level includes
        valid: True if everything loaded correctly
        inf_path: path + .inf file name
        blk_path: path + .blk file name
    """
    def __init__(self, identifier):
        """Init level objet with defaults"""
        self.set_identifier(identifier)
        self.cube_size = 32
        self.start_pos = [0, 0, 0]
        self.start_orientation = [0, 0, 0]
        self.block_data =[]
        self.valid = True

    def __str__(self):
        """String representation"""
        return self.identifier

    def set_identifier(self, identifier):
        self.identifier = identifier
        self.path = G.PATH_LEVELS + self.identifier + "/"
        self.json_path = f"{G.PATH_LEVELS}{os.sep}{self.identifier}.json"

    def print_info(self):
        """Print debug information, mainly attributes"""
        print("=== LEVEL INFORMATION ===")
        print("\tName: {}".format(self.identifier))
        print("\tCube Size: {}".format(self.cube_size))
        print("\tStart Pos: {}".format(self.start_pos))
        print("\tStart Orientation: {}".format(self.start_orientation))
        print("\tNumber of Blocks: {}".format(len(self.block_data)))

    def get_checkpoint_count(self):
        """The checkpoint count will only be set by load(), thus only get"""
        return self.__checkpoint_count

    def get_cube_size(self):
        """Returns the cube size"""
        return self.cube_size

    def get_start_pos(self):
        return self.start_pos

    def get_start_orientation(self):
        return self.start_orientation

    def is_valid(self):
        return self.valid

    def load(self):
        """
        Load the level from its folder
        This will not place any 3D objects, it will only load the level into
        memory for it to be "placed" into the 3D world.
        This is for faster level transition times:
        Levels can be loaded in advance.
        """

        sce = helpers.get_scene("Scene")
        own = logic.getCurrentController().owner

        idx = 1000

        if os.path.isfile(self.json_path):
            blk_file = json.load(open(self.json_path, "r"))
            for block in blk_file["blocks"]:
                # Get start position from start object
                if "Start" in block["type"]:
                    self.start_pos = block["position"]
                    self.start_orientation = block["orientation"]

                # Create a new block object to store the information
                block_dat = Block(
                    type=block["type"],
                    position=block["position"],
                    orientation=block["orientation"])
                if "id" in block:
                    block_dat.id = block["id"]
                else:
                    block["id"] = idx
                    idx += 1
                if "properties" in block:
                    block_dat.properties = block["properties"]

                # Append block to level block list
                self.block_data.append(block_dat)
        else:
            print("{}: {}".format(own.name, "No .json file found."))
            # self.valid = False
            # return 0

        # Sets attributes
        self.cube_size = int(blk_file["cube_size"])


    def save(self):
        """The track editor uses this to save a level to files"""
        # Save all saveable blocks

        sce = helpers.get_scene("Scene")
        own = logic.getCurrentController().owner

        blocks = []

        for obj in sce.objects:

            if "Block_" in obj.name:

                # Save the start orientation as an euler matrix
                wo = obj.worldOrientation

                block = {
                    "type" : obj.name.split('.')[0],
                    "position" : [obj.worldPosition.x,
                        obj.worldPosition.y,
                        obj.worldPosition.z],
                    "orientation" : [list(v) for v in wo],
                    "properties" : {}
                }

                # Copy properties set by the level editor into the dict
                for prop in obj.getPropertyNames():
                    try:
                        properties[prop] = block[prop]
                    except Exception as e:
                        print(e)
                blocks.append(block)

        blk_file = {
            "name": self.identifier,
            "cube_size": self.cube_size,
            "version" : logic.settings["Game"]["Version"],
            "author" : logic.settings["Player0"]["Name"],
            "blocks" : blocks}

        # with open(self.inf_path, 'w') as inffile:
        with open(self.json_path, 'w') as outfile:
            # inf.write(inffile)
            json.dump(blk_file, outfile, sort_keys = False, indent = 4)

        print("Saved level file.")
        # if G.DEBUG: print("{}: {}".format(own.name,
        #     "Saved information file."))


    def place(self):
        """
        Assuming that the level itself has been loaded in to the global dict,
        we can now actually load it into the 3D world.
        """

        sce = helpers.get_scene("Scene")
        own = logic.getCurrentController().owner

        for block in self.block_data:

            new_block = None
            try:
                new_block = sce.addObject(block.type)
            except:
                print(block.type, "not found")

            if new_block is not None:
                # Copy properties
                for prop in block.properties:
                    new_block[prop] = block.properties[prop]

                new_block.worldPosition = block.position # Set position

                # Convert Orientation to matrix and apply it to the 3D object
                # new_orientation = mathutils.Euler((0, 0, 0), "XYZ")

                # for x in [0, 1, 2]:
                #     new_orientation[x] = block.orientation[x]

                new_block.worldOrientation = mathutils.Matrix(block.orientation)

    def clear(self):
        sce = helpers.get_scene("Scene")
        self.block_data = []
        for obj in sce.objects:
            if "Block_" in obj.name:
                obj["end"] = True
                obj.endObject()

def setup():
    """Executed by the level controller object in level.blend"""

    # Create a new level
    logic.game.level = Level(logic.game.level_name)

    # Load the level data from file
    logic.game.level.load()

    if logic.game.level.is_valid():

        # Print some debug stuff
        if G.DEBUG: logic.game.level.print_info()

        # Place level in 3D world
        logic.game.level.place()

        # Make accessible in the global dict
        logic.components.mark_loaded("level")


    else:
        if G.DEBUG: print("{}: {} ({})".format(own.name,
            "The loaded level is not valid", str(new_level)))

def main():
    pass
