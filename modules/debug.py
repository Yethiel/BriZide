from bge import logic
from modules import global_constants as G

def dprint(strlist):
    if G.DEBUG: print(str(strlist))

def test():
    pass

def dump_scenes():
	print("Scenes:")
	for scene in logic.getSceneList():
		print("    {}:".format(scene.name))
		for obj in scene.objects:
			print("        {}".format(obj.name))