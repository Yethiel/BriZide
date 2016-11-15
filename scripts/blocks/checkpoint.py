from bge import logic
globalDict = logic.globalDict
from scripts.helpers import get_prop, set_prop
from scripts import global_constants as G
sce = logic.getCurrentScene()

controller_level_obj = sce.objects["Controller_Level"]


# current game mode. should be loaded from dict later.

# setup the globalDict for this checkpoint
def setup():
	own = logic.getCurrentController().owner

	# send a message that the checkpoint is ready
	logic.sendMessage("checkpoint.setup", str(own["id"]))

def actions():
	pass