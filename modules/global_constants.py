from bge import logic
import subprocess

DEBUG = True
VERSION = 0
PATH_MUSIC = logic.expandPath("//music/")
TYPES_MUSIC = [".mp3", ".ogg", ".wav"]
PLAYER_ID = 0
MOUSE_TIMEOUT = 3 # timeout for mouse dragging in the editor
REVISION = "NONE"


###

FOCUS_UI = 1
FOCUS_EDITOR_MAIN = 2
FOCUS_EDITOR_ROT = 3
FOCUS_EDITOR_GRAB = 4
FOCUS_LOCK = False


### GAMEPLAY

PORTAL_DISTANCE = 16