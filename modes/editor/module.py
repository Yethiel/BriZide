from bge import logic, events, render
from modules import btk
from modules.helpers import keystat, get_scene
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

key_select = controls["editor_select"]
key_deselect = controls["editor_deselect"]
key_delete = controls["editor_delete"]

key_rotate = controls["editor_rotate"]
key_grab = controls["editor_grab"]

# edit modes
SELECT = 0  # select and remove objects
GRAB   = 1  # move objects
ROTATE = 2  # rotate objects
ADD    = 3  # add objects to the scene


class Edit_Mode(Game_Mode):
    def __init__(self, game_obj):
        # initiates the game mode, name needs to match folder name
        super().__init__(required_components, game_obj, 'editor')
        self.selection = {}
        self.mode = SELECT  # editor starts in select mode

    def setup(self):
        """ runs after loading is done """
        super().setup()

        scene = logic.getCurrentScene()
        logic.game.set_music_dir('editor')

        # sets the camera
        scene.active_camera = scene.objects['camera_editor']

        logic.addScene('UI_Editor')

        # creates the UI
        layout = logic.ui['editor']
        label_mode = btk.Label(layout, 
            text='Mode:',
            position=[0.4, 0.4, 0],
            size=0.3,
            update=update_label_mode)

        """ Workaround:
            Libload loads all scenes from a blend file so the ones
            from overlay scenes have to be deleted manually.
            These objects are part of the overlay scene for the UI.
        """
        scene.objects['cursor'].endObject()
        scene.objects['camera_editor_ui'].endObject()

    def run(self):
        """ runs every logic tick """
        super().run()  # handles loading of components

        if logic.uim.focus == 'menu': return

        scene = logic.getCurrentScene()
        camera = scene.active_camera
        winw = render.getWindowWidth()
        winh = render.getWindowHeight()
        sensor_mouse = self.go.sensors['Over']

        # editor overlay (cursor, etc.)
        scene_ui = get_scene('UI_Editor')
        if scene_ui is None:  # skips if scene isn't loaded yet
            return
        cursor = get_scene('UI_Editor').objects['cursor']

        # synchronizes the cameras
        scene_ui.objects['camera_editor_ui'].worldPosition = camera.worldPosition
        scene_ui.objects['camera_editor_ui'].worldOrientation = camera.worldOrientation

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

        # branches out into modes
        if self.mode == SELECT:

            # rotation mode on R
            if keystat(key_rotate, 'JUST_RELEASED'):
                self.mode = ROTATE
                return

            # grab mode on G
            if keystat(key_grab, 'JUST_RELEASED'):
                self.mode = GRAB
                return

            # left shift modifier
            if keystat('LEFTSHIFTKEY', 'ACTIVE'):
                hit_obj = sensor_mouse.hitObject
                # sets the cursor to the selected object
                if keystat(key_select, 'JUST_ACTIVATED') and hit_obj != None:
                    cursor.worldPosition = hit_obj.worldPosition
                    self.select_multiple(hit_obj)
                # add object
                if keystat('AKEY', 'JUST_RELEASED'):
                    self.mode = ADD
                    return
                return

            # left control modifier
            if keystat('LEFTCTRLKEY', 'ACTIVE'):
                blocks = [obj for obj in scene.objects if "Block_" in obj.name]
                if keystat('AKEY', 'JUST_RELEASED'):
                    if len(self.selection.keys()) != len(blocks):
                        self.deselect_all()
                        for obj in blocks:
                            self.select_multiple(obj)
                    else:
                        self.deselect_all()
                return

            # selection
            hit_obj = sensor_mouse.hitObject
            if hit_obj != None:
                # sets the cursor to the selected object
                if keystat(key_select, 'JUST_ACTIVATED'):
                    cursor.worldPosition = hit_obj.worldPosition
                    self.select_single(hit_obj)

            # delete selection
            if keystat(key_delete, 'JUST_RELEASED'):
                self.delete_selection()

        elif self.mode == GRAB:
            if keystat('BACKSPACEKEY', 'JUST_RELEASED'):
                self.mode = SELECT
        elif self.mode == ROTATE:
            if keystat('BACKSPACEKEY', 'JUST_RELEASED'):
                self.mode = SELECT
        elif self.mode == ADD:
            if keystat('BACKSPACEKEY', 'JUST_RELEASED'):
                self.mode = SELECT

        # camera movement
        if keystat(key_left, 'ACTIVE'):
            camera.applyMovement([-2, 0, 0], True)
        if keystat(key_right, 'ACTIVE'):
            camera.applyMovement([2, 0, 0], True)

        if keystat(key_forward, 'ACTIVE'):
            camera.applyMovement([0, 0, -2], True)
        if keystat(key_backward, 'ACTIVE'):
            camera.applyMovement([0, 0, 2], True)

        if keystat('WHEELDOWNMOUSE', 'JUST_RELEASED'):
            camera.applyMovement([0, 0, 20], True)
        if keystat('WHEELUPMOUSE', 'JUST_RELEASED'):
            camera.applyMovement([0, 0, -20], True)

        if keystat(key_up, 'ACTIVE'):
            camera.applyMovement([0, 2, 0], True)
        if keystat(key_down, 'ACTIVE'):
            camera.applyMovement([0, -2, 0], True)

    def restart(self, widget):
        get_scene('UI_Editor').end()
        super().restart(widget)

    def delete_selection(self):
        """ Deletes all objects in the selection """
        keys = list(self.selection.keys())
        for o in keys:
            self.selection[o].endObject()
            del self.selection[o]
            o.endObject()

    def get_mode(self):
        return ['Select', 'Grab', 'Rotate', 'Add'][self.mode]

    def select_single(self, obj):
        """ Selects a single object """
        if 'Block_' not in obj.name:
            return
        scene_ui = get_scene('UI_Editor')
        self.deselect_all()
        self.selection[obj] = scene_ui.addObject('selection', obj)

    def select_multiple(self, obj):
        """ Selects multiple objects when shift is held down """
        if 'Block_' not in obj.name:
            return
        scene_ui = get_scene('UI_Editor')
        if not obj in self.selection:
            self.selection[obj] = scene_ui.addObject('selection', obj)
        else:
            self.selection[obj].endObject()
            del self.selection[obj]

    def deselect_all(self):
        keys = list(self.selection.keys())
        for o in keys:
            self.selection[o].endObject()
            del self.selection[o]


def init():
    """ Runs immediately after the scene loaded """

    # creates a new game mode object
    logic.editor = Edit_Mode(logic.getCurrentController().owner)


def main():
    logic.editor.run()


# UI functions

def update_label_mode(widget):
    widget.text = 'Mode: {}'.format(logic.editor.get_mode())
