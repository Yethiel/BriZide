from bge import logic
import subprocess

DEBUG = True
VERSION = 0
PATH_MUSIC = logic.expandPath("//music/")
TYPES_MUSIC = [".mp3", ".ogg", ".wav"]
PLAYER_ID = 0
MOUSE_TIMEOUT = 3 # timeout for mouse dragging in the editor
try:
    REVISION = str(subprocess.check_output("svn info | awk '/Revision/ { print $2; }'", shell=True)).strip("b'").strip("\\n")

except Exception as e:
    REVISION = "fuck windows"


###

FOCUS_UI = 1
FOCUS_EDITOR_MAIN = 2
FOCUS_EDITOR_ROT = 3
FOCUS_EDITOR_GRAB = 4
FOCUS_LOCK = False