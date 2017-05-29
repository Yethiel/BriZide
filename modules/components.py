"""
Load BGE Libraries sequentially so that
dependencies are met.
MAKE THIS OOP
"""

from modules import global_constants as G
from bge import logic
from time import sleep
own = logic.getCurrentController().owner

extension = G.EXTENSION_COMPONENT

class Components:
	def __init__(self):
		self.__queue = []
		self.__loaded = [None]
		self.__opened = [None]
		self.__currently_loading = None
		self.__currently_loading_str = ""
		self.__count = 0
		self.__init_loading = False

	def queue(self, components):
		"""Queue components to load them in order"""

		if isinstance(components, str):
			self.__queue.append(str(component))

		elif isinstance(components, list):
			for component in components:
				self.__queue.append(str(component))


	def load(self):
		"""Load the libraries one after another
		All libraries are loaded in a separate thread. Only one lib is loaded
		at a time.
		Run each tick!
		"""

		if not self.__init_loading and self.__queue:
			self.__init_loading = True
			self.__count = len(self.__queue)


		if self.__queue:
			# if G.DEBUG: sleep(0.2)
			if not self.__currently_loading:
				print(own.name, "Loading",self.__queue[0])
				
				# Make a path from the component name
				blend_path = logic.expandPath("{}{}{}".format(
					"//components/", self.__queue[0], extension))
				
				# Store the returned status object.
				self.__currently_loading = logic.LibLoad(blend_path, 
						"Scene", async=True)
				self.__currently_loading_str = self.__currently_loading.libraryName
				
				# Add "opened" component to the list, remove it from the queue
				self.__opened.append(self.__queue[0])
				self.__queue.pop(0)

			#Proceed with the next module when the library loaded and the 
			#component added itself to the "done" list.
			elif self.__currently_loading.finished and self.__opened[-1] == self.__loaded[-1]:
				print(own.name, "Done loading", self.__opened[-1])
				self.__currently_loading = None

		else:
			self.__init_loading = False
			self.__count = 0


	def load_immediate(self, component):
		"""Load a library immediately, blocking everything else"""

		blend_path = logic.expandPath("{}{}{}".format(
			"//components/", component, extension))

		logic.LibLoad(blend_path,"Scene", async=False)

		# self.__loaded.append(component)

	def free(self, component):
		"""Frees a component that resembles the string. Very loose."""
		for lib in logic.LibList():
			if component in lib:
				logic.LibFree(lib)

	def is_done(self, required_components):
		"""Takes a list and checks if all modules are loaded"""
		
		done = True
		for x in required_components:
			if not x in self.__loaded:
				done = False
		return done

	def is_loading(self):
		return self.__init_loading

	def mark_loaded(self, componentstr):
		if not componentstr in self.__loaded:
			self.__loaded.append(componentstr)
			return True
		else:
			return False

	def get_percent(self):
		if self.__init_loading:
			return (len(self.__loaded) / self.__count)
		else:
			return 0

	def get_currently_loading(self):
		return self.__currently_loading_str



