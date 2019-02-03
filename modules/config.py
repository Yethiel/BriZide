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
            "leveldir" : "skate_park",
            "Mode" : "time_trial",
            "version": 0
        }
        config["Player0"] = {
            "name": "Player 0",
            "Ship": "helios"
        }
        config["Audio"] = {
            "Music" : 1.0,
            "Master" : 0.8,
            "Effects" : 1.0,
        }
        config["Video"] = {
            "bloom" : "True",
            "blur" : "True",
            "fullscreen" : "False",
            "width" : 1280,
            "height" : 720,
            "transparent_tiles" : "True",
            "simple_cube" : "False",
        }

        config["Dev"] = {
            "debug" : "False",
        }

        config["Editor"] = {
            "cam_drag_amount" : 60,
        }

        config["Controls_Player1"] = {
            "ship_thrust" : "UPARROWKEY",
            "ship_thrust_reverse" : "DOWNARROWKEY",
            "ship_steer_left" : "LEFTARROWKEY",
            "ship_steer_right" : "RIGHTARROWKEY",
            "ship_boost" : "WKEY",
            "ship_deactivate_stabilizer" : "SKEY",
            "ship_pause" : "ESCKEY",
        }
        config["Controls_Editor"] = {
            "editor_confirm" : "ENTERKEY",
            "editor_discard" : "BACKSPACEKEY",
            "editor_1" : "ONEKEY",
            "editor_2" : "TWOKEY",
            "editor_3" : "THREEKEY",
            "editor_4" : "FOURKEY",
            "editor_5" : "FIVEKEY",
            "editor_6" : "SIXKEY",
            "editor_7" : "SEVENKEY",
            "editor_8" : "EIGHTKEY",
            "editor_9" : "NINEKEY",
            "editor_10" : "ZEROKEY",
            "editor_up" : "WKEY",
            "editor_down" : "SKEY",
            "editor_left" : "AKEY",
            "editor_right" : "DKEY",
            "editor_forward" : "EKEY",
            "editor_backward" : "QKEY",
            "editor_rotate_cam" : "MIDDLEMOUSE",
            "editor_next" : "PERIODKEY",
            "editor_prev" : "COMMAKEY",
            "editor_place" : "LEFTMOUSE",
            "editor_delete" : "DELKEY",
            "editor_select" : "LEFTMOUSE",
            "editor_grab" : "GKEY",
            "editor_rotate_backward" : "SKEY",
            "editor_rotate_down" : "QKEY",
            "editor_rotate_forward" : "WKEY",
            "editor_rotate_left" : "AKEY",
            "editor_rotate_right" : "DKEY",
            "editor_rotate_up" : "EKEY",
            "editor_rotate" : "RKEY",
            "editor_deselect" : "BACKSPACEKEY",
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

