"""
Load BGE Libraries sequentially so that
dependencies are met.
"""

from modules import global_constants as G
from bge import logic

own = logic.getCurrentController().owner

extension = G.EXTENSION_COMPONENT

logic.components = {
	"queue" : [],
	"loaded" : [],
	"currently_loading" : None,
	"status" : {}}


def queue(components):
	"""Queue components to load them in order"""

	if isinstance(components, str):
		logic.components["queue"].append(str(component))

	elif isinstance(components, list):
		for component in components:
			logic.components["queue"].append(str(component))


def load():
	"""Load the libraries one after another
	All libraries are loaded in a separate thread. Only one lib is loaded
	at a time.
	Run each tick.
	"""

	if logic.components["queue"]:
		if not logic.components["currently_loading"]:
			
			blend_path = logic.expandPath("{}{}{}".format(
				"//components/", logic.components["queue"][0], extension))
			
			# Store the returned status object.
			logic.components["currently_loading"] = logic.LibLoad(blend_path, 
					"Scene", async=True)
			
			print("Loading",logic.components["queue"][0])
			logic.components["queue"].pop(0)
		
		elif logic.components["currently_loading"].finished:
			logic.components["currently_loading"] = None

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

