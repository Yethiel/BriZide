from bge import logic, render
from modules import btk
from modules.game_mode import Game_Mode

required_components = ["blocklib", "blocks", "level", "cube"]


class Edit_Mode(Game_Mode):
    def __init__(self, game_obj):
        # initiates the game mode, name needs to match folder name
        super().__init__(required_components, game_obj, "editor")

    def setup(self):
        """ runs after loading is done """
        super().setup()

        scene = logic.getCurrentScene()
        logic.game.set_music_dir("editor")

        # sets the camera
        scene.active_camera = scene.objects["camera_editor"]

        # creates the UI
        layout = logic.ui["editor"]
        label_selected_block = btk.Label(layout, 
            text="block",
            position=[0.4, 0.4, 0],
            size=0.3,
            update=update_label_selected_block
        )

        self.setup_done()  # hides the loading screen


    def run(self):
        """ runs every logic tick """
        super().run()  # handles loading of components

        scene = logic.getCurrentScene()
        camera = scene.active_camera
        winw = render.getWindowWidth()
        winh = render.getWindowHeight()

        mx = logic.mouse.position[0] - 0.5
        my = logic.mouse.position[1] - 0.5

        # rotates the camera
        camera.applyRotation([0, 0.0, -mx], False)
        camera.applyRotation([-my, 0.0, 0], True)

        render.setMousePosition(int(winw / 2), int(winh / 2))     


def init():
    """ Runs immediately after the scene loaded """

    # creates a new game mode object
    logic.edit_mode = Edit_Mode(logic.getCurrentController().owner)


def main():
    logic.edit_mode.run()


# UI functions

def update_label_selected_block(widget):
    widget.text = "not implemented"