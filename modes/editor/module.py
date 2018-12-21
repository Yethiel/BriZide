from bge import logic
from modules import btk
from modules.game_mode import Game_Mode

required_components = ["blocklib", "blocks", "level", "cube"]


class Edit_Mode(Game_Mode):
    def __init__(self, game_obj):
        # initiates the game mode, name needs to match folder name
        super().__init__(required_components, game_obj, "editor")

    def setup(self):
        logic.game.set_music_dir("editor")
        super().setup()  # hides loading screen
        layout = logic.ui["editor"]

        label_selected_block = btk.Label(layout, 
            text="block",
            position=[0.4, 0.4, 0],
            size=0.3,
            update=update_label_selected_block
        )        

    def run(self):
        super().run()  # handles loading of components


def init():
    """ Runs immediately after the scene loaded """
    logic.edit_mode = Edit_Mode(logic.getCurrentController().owner)


def main():
    """ Runs every logic tick """
    logic.edit_mode.run()


# UI functions

def update_label_selected_block(widget):
    widget.text = "not implemented"