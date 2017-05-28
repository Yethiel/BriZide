"""
Load BGE Libraries sequentially so that
dependencies are met.
MAKE THIS OOP
"""

from modules import global_constants as G
from bge import logic

own = logic.getCurrentController().owner

extension = G.EXTENSION_COMPONENT

logic.components = {
	"queue" : [],
	"loaded" : [None],
	"opened" :[None],
	"currently_loading" : None}

comps = logic.components

def queue(components):
	"""Queue components to load them in order"""

	if isinstance(components, str):
		comps["queue"].append(str(component))

	elif isinstance(components, list):
		for component in components:
			comps["queue"].append(str(component))


def load():
	"""Load the libraries one after another
	All libraries are loaded in a separate thread. Only one lib is loaded
	at a time.
	Run each tick!
	"""

	if comps["queue"]:
		if not comps["currently_loading"]:
			print(own.name, "Loading",comps["queue"][0])
			
			# Make a path from the component name
			blend_path = logic.expandPath("{}{}{}".format(
				"//components/", comps["queue"][0], extension))
			
			# Store the returned status object.
			comps["currently_loading"] = logic.LibLoad(blend_path, 
					"Scene", async=True)
			
			# Add "opened" component to the list, remove it from the queue
			comps["opened"].append(comps["queue"][0])
			comps["queue"].pop(0)

		#Proceed with the next module when the library loaded and the 
		#component added itself to the "done" list.
		elif comps["currently_loading"].finished and comps["opened"][-1] == comps["loaded"][-1]:
			print(own.name, "Done loading", comps["opened"][-1])
			comps["currently_loading"] = None


def load_immediate(component):
	"""Load a library immediately, blocking everything else"""

	blend_path = logic.expandPath("{}{}{}".format(
		"//components/", component, extension))

	logic.LibLoad(blend_path,"Scene", async=False)

def free(component):
	"""Frees a component that resembles the string. Very loose."""
	for lib in logic.LibList():
		if component in lib:
			logic.LibFree(lib)

def is_done(required_components):
	"""Takes a list and checks if all modules are loaded"""
	
	done = True
	for x in required_components:
		if not x in comps["loaded"]:
			done = False
	return done

def register():
	pass