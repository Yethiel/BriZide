from bge import logic
import configparser
import os.path
from modules import global_constants as G

own = logic.getCurrentController().owner

def load():
    config = configparser.ConfigParser()
    # Check if the config file is there. If so, load it.
    if os.path.isfile(G.PATH_CONFIG_FILE):
        config.read(G.PATH_CONFIG_FILE)
        if G.DEBUG: print(own, "Successfully loaded config file.")

    else:
        # create an ini with the default configuration
        config["Game"] = {
            "Name" : "Player",
            "LevelDir" : "test",
            "Mode" : "time_trial",
        }
        config["Player0"] = {
            "name": "Player 0",
            "Ship": "test"
        }
        config["Audio"] = {
            "Music" : 1.0,
            "Master" : 1.0,
            "Effects" : 1.0,
        }

        config["Dev"] = {
        "Debug" : "True"
        }

        config["Controls_Player1"] = {
            "ship_thrust" : "UPARROWKEY",
            "ship_thrust_reverse" : "DOWNARROWKEY",
            "ship_steer_left" : "LEFTARROWKEY",
            "ship_steer_right" : "RIGHTARROWKEY",
            "ship_activate_weapon" : "LEFTCTRLKEY",
            "ship_deactivate_stabilizer" : "SPACEKEY",
            "ship_absorb_weapon" : "LEFTSHIFTKEY",
            "ship_pause" : "ESCKEY",
        }
        config["Controls_Editor"] = {
            "editor_left" : "LEFTARROWKEY",
            "editor_right" : "RIGHTARROWKEY",
            "editor_forward" : "UPARROWKEY",
            "editor_backward" : "DOWNARROWKEY",

            "editor_up" : "PAGEUPKEY",
            "editor_down" : "PAGEDOWNKEY",

            "editor_rotate_left" : "AKEY",
            "editor_rotate_right" : "DKEY",
            "editor_rotate_forward" : "WKEY",
            "editor_rotate_backward" : "SKEY",
            "editor_rotate_up" : "EKEY",
            "editor_rotate_down" : "QKEY",

            "editor_place" : "ENTERKEY",
            "editor_delete" : "DELKEY",

            "editor_next" : "PERIODKEY",
            "editor_prev" : "COMMAKEY",

            "editor_1" : "ONEKEY",
            "editor_2" : "TWOKEY",
            "editor_3" : "THREEKEY",
            "editor_4" : "FOURKEY",
            "editor_5" : "FIVEKEY",
            "editor_6" : "SIXKEY",
            "editor_7" : "SEVENKEY",
            "editor_8" : "EIGHTKEY",
            "editor_9" : "NINEKEY",
            "editor_10" : "ZEROKEY"
        }
        # create a new config file and write to it
        with open(G.PATH_CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        if G.DEBUG: print("Could not find config file. Created a file with defaults.")
    # Version number will be saved into the blk file for compatibility checks.
    config["Game"]["Version"] = str(G.VERSION)
    return config


def save():
    config = logic.settings
    
    with open(G.PATH_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
        if G.DEBUG: print("Settings saved")

