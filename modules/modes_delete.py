from bge import logic
from os import listdir
import configparser

sce = logic.getCurrentScene()
cont = logic.getCurrentController()
own = cont.owner

def load(mode):
    inf_path = logic.expandPath("//modes/"+mode+"/"+mode+".inf")

    # load the information file
    inf = configparser.ConfigParser()
    if os.path.isfile(inf_path):
        inf.read(inf_path)
        print("Loaded game mode information file.")

def start(mode):
    pass
    # load lib
