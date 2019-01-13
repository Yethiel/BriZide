"""
This is the script for the E D I T O R.
Be careful with this. If you change too many things, others might not be able to open your tracks.
It is attached to the Controller object in the mode's blend file.
"""

from bge import logic
from modules import btk, level, components, global_constants as G
# from modules.ui_editor import EditorUI

globalDict = logic.globalDict
own = logic.getCurrentController().owner # This is the object that executes these functions.

own["init"] = False

required_components = ["blocklib", "blocks", "level", "cube", "ship"]
queue_id = logic.components.enqueue(required_components)

# Setup is executed as soon as the game mode has been loaded.
def setup():
    
    ### Prepare the global dict
    editor = {
        "selected_block" : "Block_0_32_32_32" # yay defaults
    }
    globalDict["editor"] = editor

    # Queue the required components

    # Set the music directory
    logic.game.set_music_dir("editor")

    # the blocklib will free itself after main() is done.
    # logic.addScene("UI_Editor")

    # unlock ship
    logic.uim.set_focus("editor_main")


def update_label_selected_block(widget):
    widget.text = globalDict["editor"]["selected_block"]

# The main loop always runs.
def main():
    
    if not own["init"]:

        # Prepare the game mode by loading the queued components
        logic.components.load()

        # If the queue is emtpy, we're done
        if logic.components.is_done(required_components):
            own["init"] = True
            setup()
    else:
        pass
