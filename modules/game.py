
import os
from bge import logic

from modules import components, config
from modules import global_constants as G

globalDict = logic.globalDict

class Game:
    """
    Class for all the things that are going on while the game is running.
    It is used to manage ships and their players, available content and
    the level object.
    """
    def __init__(self, game_obj):
        self.ships = {}           # dictionary of ships (id:ship)
        self.level = None           # current level object
        self.level_name = logic.settings["Game"]["leveldir"]
        self.mode = logic.settings["Game"]["mode"]            # current mode (string)
        self.music_dir = None       # current music directory (string)
        self.block_list = []
        self.ship_possessions = {}  # dictionary player_id:ship_id
        self.players = [0]

        # lists for game content (strings of folder names)
        self.level_list = []
        self.ship_list = []
        self.mode_list = []

        self.go = game_obj

    def register_ship(self, objref):
        """
        Called by each ship to link itself in the ships dictionary
        Returns a unique id that is used to link the ship to a player.
        """
        ship_id = len(self.ships)
        self.ships[ship_id] = objref
        return ship_id

    def set_ship(self, ship_str):
        logic.settings["Player0"]["ship"] = ship_str
        return ship_str

    def get_ship(self, ship_id):
        """Get the ship object with the id (int)"""
        return self.ships[ship_id]

    def assign_ship_to_player(self, ship_id, player_id):
        """Assigns ship id to player id"""
        self.ship_possessions[player_id] = ship_id
        if G.DEBUG: print("GAME: Assigned ship {} to player {}".format(
            ship_id, player_id))
        return self.ship_possessions[player_id]

    def get_ship_by_player(self, player_id):
        """Returns ship object assigned to player id"""
        if player_id in self.ship_possessions:
            return self.get_ship((self.ship_possessions[player_id]))
        else:
            return False

    def set_level(self, levelstr):
        """Set the folder name of the level"""
        logic.settings["Game"]["leveldir"] = levelstr
        self.level_name = levelstr
        return levelstr

    def get_level(self):
        """Returns the level object"""
        return self.level

    def set_mode(self, modestr):
        """Sets the mode (takes folder name of game mode)"""
        logic.settings["Game"]["mode"] = modestr
        self.mode = modestr
        return modestr

    def get_mode(self):
        """Returns the folder name of the currently set mode"""
        return self.mode

    def set_music_dir(self, dirstr):
        """Set the music directory (subdir of music folder)"""
        self.music_dir = dirstr
        return self.music_dir

    def get_music_dir(self):
        """Returns the current music directory"""
        return self.music_dir

    def get_profile_dir(self, player_id="0"):
        return os.path.join(G.PATH_PROFILES, logic.settings["Player{}".format(player_id)]["Name"])

    def start(self):
        """Starts the game (tells the game mode to start and load all comps)"""
        if G.DEBUG: print("Starting game")
        logic.components.load_immediate(
            "../modes/" + self.mode + "/" + self.mode)

    def clear(self):
        self.ships = {}           # dictionary of ships (id:ship)
        self.level = None           # current level object
        self.level_name = logic.settings["Game"]["leveldir"]
        self.block_list = []
        self.ship_possessions = {}  # dictionary player_id:ship_id
        self.players = [0]

    def save_settings(self):
        config.save()