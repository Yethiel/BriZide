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

def add():
    """
    This will look up all objects in a blend file and append them to the block list.
    """

    # gets all blocks that are in this scene and add them to a list
    for obj in sce.objects:
        if "Block_" in obj.name:
            logic.game.block_list.append(obj.name)

    if len(logic.game.block_list) != 0: # if some blocks have been found
        if G.DEBUG:
            print("Successfully loaded block list.")
            print(logic.game.block_list)

    for obj in sce.objects:
        if "Block" in obj.name or "LOD" in obj.name:
            obj.endObject()

def main():
    """
    Gets executed by the Controller object.
    The library will be freed shortly after.
    """
    add()
    logic.components.mark_loaded("blocklib")
