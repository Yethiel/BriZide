from bge import logic
from modules import helpers, global_constants as G


def setup():
    sce = helpers.get_scene("Scene")
    own = logic.getCurrentController().owner
    light_obj = sce.objects[own["light"]]
    light_obj.worldPosition = own.worldPosition

def main():
    sce = helpers.get_scene("Scene")
    own = logic.getCurrentController().owner
    light_obj = sce.objects[own["light"]]
    light_obj.worldPosition = own.worldPosition
    light_obj.worldOrientation = own.worldOrientation
