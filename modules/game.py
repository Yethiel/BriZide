from bge import logic

from modules import components

class Game:
	"""
	This class is meant to act like the globalDict, mostly because I cannot keep
	track of all the properties.
	"""
	def __init__(self):
		self.__ships = {}	# dictionary of ships (id:ship)
		self.level = None
		self.mode = None

		# lists for game content
		self.level_list = []
		self.ship_list = []
		self.mode_list = []

	def register_ship(self, objref):
		"""Returns an ID and saves a reference in the dictionary"""
		ship_id = len(self.__ships)
		self.__ships[ship_id] = objref
		return ship_id

	def set_level(self, levelstr):
		"""Set the folder name of the level"""
		self.level = levelstr
		return levelstr

	def get_level(self):
		return self.level

	def set_mode(self, modestr):
		self.mode = modestr
		return modestr

	def get_mode(self):
		return self.mode

	def start(self):
		"""Starts the game"""
		logic.components.load_immediate("../modes/" + self.mode + "/" + self.mode)
