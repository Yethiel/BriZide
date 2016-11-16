"""
These are just some scripts to make loading libraries (components) easier.
"""
from modules import global_constants as G
from bge import logic
extension = ".blend"
def load(component):
	logic.LibLoad(logic.expandPath("//components/"+component+extension), "Scene")
	if G.DEBUG: print("Loaded component " + component)

# Frees a component
def free(component):
	for lib in logic.LibList():
		if component in lib:
			logic.LibFree(lib)
			if G.DEBUG: print("Freed component " + component)
