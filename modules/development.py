import os
import shutil
from bge import logic
from modules import global_constants as G

def clean_files(p=G.PATH_GAME):       
    for f in os.listdir(p):
        curpath = os.path.join(p, f)
        if f == "__pycache__":
            shutil.rmtree(curpath)
        elif ".blend1" in f:
            os.remove(curpath)
        elif ".blend2" in f:
            os.remove(curpath)
        elif os.path.isdir(curpath):
            clean_files(curpath)
    print("Successfully cleaned files for release.")

def dump_scenes():
    print("Scenes:")
    for scene in logic.getSceneList():
        print("    {}:".format(scene.name))
        for obj in scene.objects:
            print("        {}".format(obj.name))
