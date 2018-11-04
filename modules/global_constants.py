from bge import logic
import datetime

now = datetime.datetime.now()

### META
DEBUG = True
VERSION = 0
REVISION = now.strftime("%Y-%m-%d %H:%M")

### CONTENT PATHS
PATH_LEVELS = logic.expandPath("//levels/")
PATH_SHIPS = logic.expandPath("//ships/")
PATH_MODES = logic.expandPath("//modes/")
PATH_MUSIC = logic.expandPath("//music/")
PATH_CONFIG_FILE = logic.expandPath("//config.ini")

### FILE TYPES
TYPES_MUSIC = [".mp3", ".ogg", ".wav", ".flac"]
EXTENSION_COMPONENT = ".blend"
EXTENSION_INF = ".inf"
EXTENSION_BLK = ".blk"
EXTENSION_BLD = ".blend"

### INPUT FOCUS CONSTANTS
FOCUS_UI = 1
FOCUS_EDITOR_MAIN = 2
FOCUS_EDITOR_ROT = 3
FOCUS_EDITOR_GRAB = 4
FOCUS_LOCK = False

### EDITOR
MOUSE_TIMEOUT = 3 # timeout for mouse dragging in the editor

### GAMEPLAY
PLAYER_ID = 0
PORTAL_DISTANCE = 16