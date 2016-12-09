"""
This is the script for the free game mode.
It is attached to the Controller object in the mode's blend file.
"""

from bge import logic, events
from modules import components, global_constants as G

sce = logic.getCurrentScene() # Scene that contains all objects
own = logic.getCurrentController().owner # Object that controls this module
gD = logic.globalDict # globalDict for saving things across objects

own["init"] = False

required_components = ["blocks", "level", "cube", "ship"]

# Queue the required components
queue_id = components.queue(required_components)

# Set the music directory
# gD["current"]["music"]["subdir"] = "free"

def setup():
	
	# Setup the game mode and give the player controls.
	own["Timer"] = 0
	gD["input"]["focus"] = "ship"
	
	# In debug mode, print when game mode is ready
	if G.DEBUG: print("{}: {}".format(own.name, "Free mode has been set up."))

# The main loop always runs.
def main():

	if not own["init"]:

		# Prepare the game mode by loading the queued components
		components.load()

		# If the queue is emtpy, we're done
		if components.is_done(required_components):
			own["init"] = True
			setup()
	else:
		pass


def controls():
	pass
