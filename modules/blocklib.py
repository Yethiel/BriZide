"""
The blocklib is only used to get a list of all avaiable blocks.
It is also linked to the blocks component which links to the Blocks group of
blocklib.blend to the second layer of blocks.blend so they can be used with
addObj.
"""
from bge import logic

co = logic.getCurrentController()
own = co.owner
sce = logic.getCurrentScene()

settings = logic.globalDict.get("settings")
DEBUG = settings["Dev"]["debug"] == "True"

# Add all blocks to the gobal dict
def add():
	# load the block list from the globalDict (in case multiple blocklibs are used, so that these can be added to the list, we don't want to replace it)
	block_list = logic.globalDict.get("current")["block_list"]

	# get all blocks that are in this scene and add them to a list
	for obj in sce.objects:
		if "Block_" in obj.name:
			# we need to use the name since this lib will be freed and the objects will be gone, leaving freed references
			block_list.append(obj.name)
	logic.globalDict["current"]["block_list"] = block_list # save the list back to the globalDict
	if len(block_list) != 0: # if there is actually something there...
		print("Successfully loaded block list.")
		if DEBUG: print(block_list)

def free_component(component):
	for lib in logic.LibList():
		if component in lib:
			logic.LibFree(lib)
			print("Freed component " + component)

def main():
	add()
	# free the lib since blocklib is on the first layer while we need it to be on the second layer for addObject
	free_component("blocklib")
