import os
import shutil
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
