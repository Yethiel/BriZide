import os
from bge import logic, events
from modules import level, global_constants as G, sound, helpers

from random import randint

import sys
import bgui
import bgui.bge_utils

required_components = ["blocks", "level", "cube", "ship"]

# Queue the required components
components = logic.components
queue_id = components.enqueue(required_components)

sce = logic.getCurrentScene() # scene that contains all objects
gD = logic.globalDict

own = logic.getCurrentController().owner # This is the object that executes these functions.

own["init"] = False

TRIGGER_DISTANCE = 32 # distance for a checkpoint to be triggered

own["countdown"] = 4

own["init_cp"] = False # whether the checkpoints have been set up


# Setup is executed as soon as the game mode has been loaded.

keyboard = logic.keyboard
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

#Key assignments Keyboard, will be loaded from settings
key_reset = events.BACKSPACEKEY
key_restart = events.DELKEY
# key_menu_confirm = events.ENTERKEY


class TimeTrialUI(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)
        self.frame = bgui.Frame(self, border=0)
        self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

        self.lbl_count = bgui.Label(self.frame, text="1", pos=[0.5, 0.7], sub_theme='Large', options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        #self.lbl_laps = bgui.Label(self.frame, text="Lap", pos=[0.2, 0.9], options = bgui.BGUI_DEFAULT)
        self.lbl_checkpoints = bgui.Label(self.frame, text="0/0", pos=[0.2, 0.85], options = bgui.BGUI_DEFAULT)
        self.lbl_time = bgui.Label(self.frame, text="", pos=[0.5, 0.85], sub_theme='Large', options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)
        #self.lbl_time_last_check = bgui.Label(self.frame, text="Time", pos=[0.5, 0.75], options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)

    def update(self):
        self.lbl_checkpoints.text = "Chk " + str(gD["time_trial"]["cp_progress"][str(0)]) +"/"+ str(gD["time_trial"]["cp_count"])

        if own["countdown"] < 4:
            self.lbl_count.text = str(own["countdown"])
        else:
            self.lbl_count.text = ""
        if own["countdown"] == 0:
            self.lbl_count.text = "GO!"
        if own["countdown"] == -1:
            self.lbl_count.text = ""

        if own["CountdownTimer"] > 4 and gD:
            if not gD["time_trial"]["cp_count"] == gD["time_trial"]["cp_progress"]["0"]:
                self.lbl_time.text = helpers.time_string(own["Timer"])


# The main loop always runs.
def main():

    if not own["init"]:

        # Prepare the game mode by loading the queued components
        components.load()

        # If the queue is emtpy, we're done
        if components.is_done(required_components):
            own["init"] = True
            setup()
    else:
        pass

    cp_data = gD["time_trial"]["checkpoint_data"]


    if own["countdown"] > -1 and own["CountdownTimer"] > 1:
        if own["countdown"] == 4:
            sound.play("three" + str(randint(0,4)))
            # sound.EchoWrapper("three0").play()
            own["countdown"] -= 1
        if own["countdown"] == 3 and own["CountdownTimer"] > 2:
            sound.play("two" + str(randint(0,4)))
            own["countdown"] -= 1
        if own["countdown"] == 2 and own["CountdownTimer"] > 3:
            sound.play("one" + str(randint(0,4)))
            own["countdown"] -= 1
        if own["countdown"] == 1 and own["CountdownTimer"] > 4:
            # sound.play("go" + str(randint(0,4)))
            sound.EchoWrapper("go" + str(randint(0,4))).play()
            own["countdown"] -= 1
            # Give controls to the player
            gD["input"]["focus"] = "ship"
            own["Timer"] = 0.0
        if own["countdown"] == 0 and own["CountdownTimer"] > 5:
            own["countdown"] -= 1

    for cp in cp_data:
        for ship in logic.game.ships:
            if logic.game.ships[ship].getDistanceTo(cp) <= TRIGGER_DISTANCE:
                if not str(ship) in cp:
                    cp[str(ship)] = True
                    sound.play("checkpoint")
                    if G.DEBUG: print("Ship", ship, "passed", cp_data.index(cp))

                    amnt_passed = 0
                    for cp in cp_data:
                        if str(ship) in cp:
                            amnt_passed += 1
                    
                    if G.DEBUG: print(amnt_passed, "/", len(cp_data))
                    
                    gD["time_trial"]["cp_progress"][str(ship)] = amnt_passed
                    if amnt_passed == len(cp_data):
                        gD["input"]["focus"] = "menu"

                        if G.DEBUG: print("Time Trial over.")

                        gD["time_trial"]["final_time"] = own["Timer"]
                        write_score()

                        sound.play("race_complete")


def write_score():
    tt_file_path = os.path.join(logic.game.get_profiles_dir(), "time_trial.txt")

    with open(tt_file_path, "a") as f:
        f.write(str(gD["time_trial"]["final_time"]) + '\n')


def setup():

    # a dict to store all data we need
    gD["time_trial"] = {}
    gD["time_trial"]["checkpoint_data"] = []
    gD["time_trial"]["cp_count"] = 0
    gD["time_trial"]["cp_progress"] = {"0":0}

    cp_data = gD["time_trial"]["checkpoint_data"]

    for obj in sce.objects:
        if "Block_Checkpoint" in obj.name:
            cp_data.append(obj)
            gD["time_trial"]["cp_count"] = len(cp_data)
    print("AMOUNT CHECKPOINTS", len(cp_data))

    logic.ui["sys"].add_overlay(TimeTrialUI)

    logic.game.set_music_dir("time_trial")

    # In debug mode, print when game mode is ready
    if G.DEBUG: print(own.name + ": Game mode Time Trial has been set up.")

    own["Timer"] = 0


def controls():
    pass


