from bge import logic, render
from modules import btk
from modules.game_mode import Game_Mode

required_components = ["blocks", "level", "cube", "ship"]


class Free_Mode(Game_Mode):
    def __init__(self, game_obj):
        # initiates the game mode, name needs to match folder name
        super().__init__(required_components, game_obj, "free")

    def setup(self):
        """ runs after loading is done """
        super().setup()
        logic.game.set_music_dir("time_trial")
        logic.uim.set_focus("ship")

    def run(self):
        """ runs every logic tick """
        super().run()  # handles loading of components


def init():
    """ Runs immediately after the scene loaded """
    logic.free_mode = Free_Mode(logic.getCurrentController().owner)

def main():
    logic.free_mode.run()
