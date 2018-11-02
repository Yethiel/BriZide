"""
This module is for managing levels.
Objects from the classes defined here will be saved in the gD.
"""

import os
import pickle
import configparser
import mathutils
from bge import logic
from modules import global_constants as G


cont = logic.getCurrentController()
sce = logic.getCurrentScene()
own = cont.owner

gD = logic.globalDict

settings = gD.get("settings")

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
        __cube_size: Size of the cube that encloses the level
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
        self.path = G.PATH_LEVELS + self.identifier + "/"
        self.__cube_size = 32
        self.__start_pos = [0, 0, 0]
        self.__start_orientation = [0, 0, 0]
        self.__block_data =[]
        self.__valid = True

        self.inf_path = self.path + self.identifier + G.EXTENSION_INF
        self.blk_path = self.path + self.identifier + G.EXTENSION_BLK
        self.blend_path = self.path + self.identifier + G.EXTENSION_BLD

    def __str__(self):
        """String representation"""
        return self.identifier

    def print_info(self):
        """Print debug information, mainly attributes"""
        print("=== LEVEL INFORMATION ===")
        print("\tName: {}".format(self.identifier))
        print("\tCube Size: {}".format(self.__cube_size))
        print("\tStart Pos: {}".format(self.__start_pos))
        print("\tStart Orientation: {}".format(self.__start_orientation))
        print("\tNumber of Blocks: {}".format(len(self.__block_data)))

    def get_checkpoint_count(self):
        """The checkpoint count will only be set by load(), thus only get"""
        return self.__checkpoint_count

    def get_cube_size(self):
        """Returns the cube size"""
        return self.__cube_size

    def get_start_pos(self):
        return self.__start_pos

    def get_start_orientation(self):
        return self.__start_orientation

    def is_valid(self):
        return self.__valid

    def load(self):
        """
        Load the level from its folder
        This will not place any 3D objects, it will only load the level into
        memory for it to be "placed" into the 3D world.
        This is for faster level transition times:
        Levels can be loaded in advance.
        """

        idx = 1000

        # Load the information file
        if os.path.isfile(self.inf_path):
            inf_file = configparser.ConfigParser()
            inf_file.read(self.inf_path)
            if G.DEBUG: print("{}: {}".format(own.name,
                "Loaded level information file."))
        else:
            if G.DEBUG: print("{}: {} ({})".format(own.name,
                "Could not load level information file.",
                self.inf_path))
            self.__valid = False
            return 0

        # Load the Blend file
        if os.path.isfile(self.blend_path):
            logic.LibLoad(self.blend_path,"Scene")
            print("{}: {}".format(own.name, "Loaded .blend file."))
        # Load the block file
        if os.path.isfile(self.blk_path):
            blk_file = pickle.load(open(self.blk_path, "rb"))
            for block in blk_file["blocks"]:
                # Get start position from start object
                if "Start" in block["type"]:
                    self.__start_pos = block["position"]
                    self.__start_orientation = block["orientation"]

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
                self.__block_data.append(block_dat)
        else:
            print("{}: {}".format(own.name, "No .blk file found."))
            # self.__valid = False
            # return 0


        # Set attributes
        self.__cube_size = int(inf_file["meta"]["cube_size"])

    def save(self):
        """The track editor uses this to save a level to files"""
        # Save all saveable blocks
        for obj in sce.objects:

            if "Block_" in obj.name:

                # Save the start orientation as an euler matrix
                wo = obj.worldOrientation.to_euler()

                block = {
                    "type" : obj.meshes[0].name,
                    "position" : [obj.worldPosition.x,
                        obj.worldPosition.y,
                        obj.worldPosition.z],
                    "orientation" : [wo[0], wo[1], wo[2]],
                    "properties" : {}
                }

                # Copy properties set by the level editor into the dict
                for prop in obj.getPropertyNames():
                    properties[prop] = block[prop]

                blocks.append(block)

        blk_file = {
            "version" : settings["Game"]["Version"],
            "author" : settings["Game"]["Name"],
            "blocks" : blocks}

        # TODO(Yethiel): Make up own format
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

        if G.DEBUG: print("{}: {}".format(own.name,
            "Saved information file."))


    def place(self):
        """
        Assuming that the level itself has been loaded in to the global dict,
        we can now actually load it into the 3D world.
        """
        for block in self.__block_data:

            new_block = sce.addObject(block.type)

            # Copy properties
            for prop in block.properties:
                new_block[prop] = block.properties[prop]

            new_block.worldPosition = block.position # Set position

            # Convert Orientation to matrix and apply it to the 3D object
            new_orientation = mathutils.Euler((0, 0, 0), "XYZ")

            for x in [0, 1, 2]:
                new_orientation[x] = block.orientation[x]

            new_block.worldOrientation = new_orientation.to_matrix()

def setup():
    """Executed by the level controller object in level.blend"""

    # Create a new level
    new_level = Level(settings["Game"]["leveldir"])

    # Load the level data from file
    new_level.load()

    if new_level.is_valid():

        # Print some debug stuff
        if G.DEBUG: new_level.print_info()

        # Place level in 3D world
        new_level.place()

        # Make accessible in the global dict
        logic.game.set_level(new_level)
        logic.components.mark_loaded("level")


    else:
        if G.DEBUG: print("{}: {} ({})".format(own.name,
            "The loaded level is not valid", str(new_level)))

def main():
    pass
