"""
The blocklib is only used to get a list of all avaiable blocks.
It is also linked to the blocks component which links to the Blocks group of
blocklib.blend to the second layer of blocks.blend so they can be used with
addObj.
"""
from bge import logic
from modules import global_constants as G

cont = logic.getCurrentController()
own = cont.owner
sce = logic.getCurrentScene()


settings = logic.globalDict.get("settings")

def add():
    """
    This will look up all objects in a blend file and append them to the block list.
    """
    # load the block list from the globalDict (in case multiple blocklibs are used, so that these can be added to the list, we don't want to replace it)
    block_list = logic.game.block_list

    # get all blocks that are in this scene and add them to a list
    for obj in sce.objects: 
        if "Block_" in obj.name:
            # we need to use the name since this lib will be freed and the objects will be gone, leaving freed references
            block_list.append(obj.name)

    if len(block_list) != 0: # if some blocks have been foudn
        if G.DEBUG:
            print("Successfully loaded block list.")
            print(block_list)

def main():
    """
    Gets executed by the Controller object.
    The library will be freed shortly after.
    """
    add()
    logic.components.mark_loaded("blocklib")

