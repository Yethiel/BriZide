"""
These are just some functions to make loading libraries (components) easier.
"""

from modules import global_constants as G
from bge import logic
extension = G.EXTENSION_COMPONENT

def load(component):
	"""
	Loads a component
	:param: component: Exact file name of the component without extension
	"""
	logic.LibLoad(logic.expandPath("//components/"+component+extension), "Scene")
	if G.DEBUG: print("Loaded component " + component)

def free(component):
	"""
	Frees a component
	:param: component: Component name
	"""
	for lib in logic.LibList():
		if component in lib:
			logic.LibFree(lib)
			if G.DEBUG: print("Freed component " + component)
