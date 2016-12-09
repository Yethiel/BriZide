from bge import logic
from modules import global_constants as G
gD = logic.globalDict
sce = logic.getCurrentScene()

def setup():
	own = logic.getCurrentController().owner
	# send a message that the checkpoint is ready
	try:
		logic.sendMessage("checkpoint.setup", str(own["id"]))
	except:
		pass

def actions():
	pass
