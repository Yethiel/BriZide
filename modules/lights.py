from bge import logic

from modules import helpers, global_constants as G


def setup():
    sce = helpers.get_scene("Scene")
    print(sce.name)
    own = logic.getCurrentController().owner
    light_obj = sce.objects[own["light"]]
    light_obj.worldPosition = own.worldPosition

    # light_obj.setParent(own) bork
    # light_obj["light_obj"] = True

def main():
    sce = helpers.get_scene("Scene")
    own = logic.getCurrentController().owner
    light_obj = sce.objects[own["light"]]
    light_obj.worldOrientation = own.worldPosition
    light_obj.worldOrientation = own.worldOrientation
