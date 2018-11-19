from bge import logic

from modules import global_constants as G

logic.lights = []

def setup():
    sce = logic.getCurrentScene()
    own = logic.getCurrentController().owner
    light_obj = sce.objects[own["light"]]
    light_obj.worldPosition = own.worldPosition
    light_obj.worldOrientation = own.worldOrientation

    light_obj.setParent(own)

    logic.lights.append(light_obj)


def clear():
    sce = logic.getCurrentScene()
    own = logic.getCurrentController().owner

    if G.DEBUG: print("Clearing lights")

    for obj in logic.lights:
        obj.removeParent()
        logic.lights.remove(obj)