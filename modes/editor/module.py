from bge import logic, events, render
from modules import btk
from modules.helpers import keystat
from modules.game_mode import Game_Mode

required_components = ["blocklib", "blocks", "level", "cube"]
kbd = logic.keyboard
mouse = logic.mouse

controls = logic.settings["Controls_Editor"]

key_rotate_cam = controls["editor_rotate_cam"]
key_left = controls["editor_left"]
key_right = controls["editor_right"]
key_forward = controls["editor_forward"]
key_backward = controls["editor_backward"]
key_up = controls["editor_up"]
key_down = controls["editor_down"]


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

    def run(self):
        """ runs every logic tick """
        super().run()  # handles loading of components

        scene = logic.getCurrentScene()
        camera = scene.active_camera
        winw = render.getWindowWidth()
        winh = render.getWindowHeight()

        # camera rotation
        if keystat(key_rotate_cam, 'JUST_ACTIVATED'):
            mouse.visible = False
            self.old_mouse_pos = logic.mouse.position
            render.setMousePosition(int(winw / 2), int(winh / 2))     

        if keystat(key_rotate_cam, 'ACTIVE'):
            render.setMousePosition(int(winw / 2), int(winh / 2))     
            mx = logic.mouse.position[0] - 0.5  # how much the mouse moved
            my = logic.mouse.position[1] - 0.5
            camera.applyRotation([0, 0.0, -mx], False)
            camera.applyRotation([-my, 0.0, 0], True)

        if keystat(key_rotate_cam, 'JUST_RELEASED'):
            render.setMousePosition(
                int(self.old_mouse_pos[0] * winw), 
                int(self.old_mouse_pos[1] * winh))
            mouse.visible = True

        if keystat(key_left, 'ACTIVE'):
            camera.applyMovement([-1, 0, 0], True)
        if keystat(key_right, 'ACTIVE'):
            camera.applyMovement([1, 0, 0], True)

        if keystat(key_forward, 'ACTIVE'):
            camera.applyMovement([0, 0, -1], True)
        if keystat(key_backward, 'ACTIVE'):
            camera.applyMovement([0, 0, 1], True)

        if keystat(key_up, 'ACTIVE'):
            camera.applyMovement([0, 1, 0], True)
        if keystat(key_down, 'ACTIVE'):
            camera.applyMovement([0, -1, 0], True)

def init():
    """ Runs immediately after the scene loaded """

    # creates a new game mode object
    logic.edit_mode = Edit_Mode(logic.getCurrentController().owner)


def main():
    logic.edit_mode.run()


# UI functions

def update_label_selected_block(widget):
    widget.text = "not implemented"