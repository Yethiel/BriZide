"""
These functions will go through the folders and search for (user) content.
set_all() will set the entry in the globalDict
Mainly used for frontend to load with components.py or modes.py.

TL;DR: Get name lists of available content
"""
from bge import logic
import os
from modules import global_constants as G


def get_levels():
    """Returns a list of level folder names"""
    levels = []
    for folder in os.listdir(G.PATH_LEVELS):
        if folder+".inf" in os.listdir(logic.expandPath(G.PATH_LEVELS+folder)):
            levels.append(folder)
    return levels


def get_ships():
    """Returns a list of ship folder names"""
    ships = []
    for folder in os.listdir(G.PATH_SHIPS):
        if folder+".inf" in os.listdir(logic.expandPath(G.PATH_SHIPS+folder)):
            ships.append(folder)
            logic.LibLoad(os.path.join(logic.expandPath(G.PATH_SHIPS+folder), folder) + ".blend", "Mesh")

    return ships


def get_modes():
    """Returns a list of game mode folder names"""
    modes = []
    for folder in os.listdir(G.PATH_MODES):
        if os.path.isdir(logic.expandPath(G.PATH_MODES+folder)) and folder+".inf" in os.listdir(logic.expandPath(G.PATH_MODES+folder)):
            modes.append(folder)
    return modes


def set_all():
    """Calls all the get functions and sets the lists."""
    logic.game.level_list = get_levels()
    logic.game.ship_list = get_ships()
    logic.game.mode_list = get_modes()
