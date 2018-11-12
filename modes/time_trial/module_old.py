import os
from bge import logic, events
from modules import components, level, global_constants as G, sound, helpers, ui, ui_main_menu

from random import randint

import sys
import bgui
import bgui.bge_utils

required_components = ["blocks", "level", "cube", "ship"]
TRIGGER_DISTANCE = 32 # distance for a checkpoint to be triggered
gD = logic.globalDict
game = logic.game

# a dict to store all data we need
gD["time_trial"] = {}
gD["time_trial"]["checkpoint_data"] = []
gD["time_trial"]["cp_count"] = 0
gD["time_trial"]["cp_progress"] = {"0":0}
gD["time_trial"]["best_times"] = []
gD["time_trial"]["best_time"] = ("nobody", 999.999)

own = logic.getCurrentController().owner # This is the object that executes these functions.
own["countdown"] = 4
own["init_cp"] = False # whether the checkpoints have been set up


def init():

    # Queue the required components
    logic.components = components.Components()
    queue_id = logic.components.enqueue(required_components)

    sce = logic.getCurrentScene() # scene that contains all objects
    own = logic.getCurrentController().owner # This is the object that executes these functions.

    own["init"] = False

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

        self.lbl_count = bgui.Label(
            self.frame, 
            text="1", 
            pos=[0.5, 0.7], 
            sub_theme='Large', 
            options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX
        )
        self.lbl_checkpoints = bgui.Label(
            self.frame, 
            text="0/0", 
            pos=[0.2, 0.85], 
            options = bgui.BGUI_DEFAULT
        )
        self.lbl_time = bgui.Label(
            self.frame, 
            text="", 
            pos=[0.5, 0.85], 
            sub_theme='Large', 
            options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX
        )
        self.lbl_best = bgui.Label(
            self.frame, 
            text="BEST: {} ({})".format(helpers.time_string(gD["time_trial"]["best_time"][1]), gD["time_trial"]["best_time"][0]),
            pos=[0.5, 0.82], 
            options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX
        )

        self.button_menu = bgui.FrameButton(self.frame,
                text="Back to Menu",
                size=[.2, .1],
                pos=[0.5, .3],
                options = bgui.BGUI_DEFAULT
        )

        self.button_menu.on_click = self.return_to_menu
        self.button_menu.visible = False

    def return_to_menu(self, widget):

        sce = logic.getCurrentScene() # scene that contains all objects
        own = logic.getCurrentController().owner # This is the object that executes these functions.


        logic.ui["sys"].remove_overlay(TimeTrialUI)
        logic.ui["sys1"].remove_overlay(ui.OverlayUI)
        for component in required_components:
            logic.components.free(component)
        own.endObject()
        logic.components.free("time_trial")
        logic.ui["sys"].add_overlay(ui_main_menu.MainMenu)


    def update(self):

        sce = logic.getCurrentScene() # scene that contains all objects
        own = logic.getCurrentController().owner # This is the object that executes these functions.

        if "init" in own and own["init"]:

            self.lbl_checkpoints.text = "Chk " + str(gD["time_trial"]["cp_progress"][str(0)]) +"/"+ str(gD["time_trial"]["cp_count"])

            if not "countdown" in own:
                own["countdown"] = 4

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

            amnt_passed = gD["time_trial"]["cp_progress"]["0"]
            if amnt_passed == len(gD["time_trial"]["checkpoint_data"]):
                self.button_menu.visible = True
            else:
                self.button_menu.visible = False
                


# The main loop always runs.
def main():

    sce = logic.getCurrentScene() # scene that contains all objects
    own = logic.getCurrentController().owner # This is the object that executes these functions.

    if not "init" in own:
        own["init"] = False

    if not own["init"]:

        # Prepare the game mode by loading the queued components
        logic.components.load()

        # If the queue is emtpy, we're done
        if logic.components.is_done(required_components):
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
                        write_time()

                        sound.play("race_complete")



def write_time():
    tt_file_path = os.path.join(logic.game.get_profiles_dir(),"time_trial", "{}.txt".format(logic.game.level_name))

    with open(tt_file_path, "a") as f:
        f.write(str(gD["time_trial"]["final_time"]) + '\n')

def get_times():
    for player in os.listdir(G.PATH_PROFILES):
        score_file = os.path.join(G.PATH_PROFILES, player, "time_trial", "{}.txt".format(game.level_name))
        print(score_file)
        if os.path.isfile(score_file):
            with open(score_file, "r") as f:
                for line in f:
                    gD["time_trial"]["best_times"].append((player, float(line)))
        elif G.DEBUG:
            print("Score file does not exist")

def get_best_time():
    gD["time_trial"]["best_time"]
    for time in gD["time_trial"]["best_times"]:
        if time[1] < gD["time_trial"]["best_time"][1]:
            gD["time_trial"]["best_time"] = time

    return gD["time_trial"]["best_time"]


def setup():

    sce = logic.getCurrentScene() # scene that contains all objects
    own = logic.getCurrentController().owner # This is the object that executes these functions.

    cp_data = gD["time_trial"]["checkpoint_data"]


    if not os.path.isdir(os.path.join(game.get_profiles_dir(),"time_trial")):
        os.makedirs(os.path.join(game.get_profiles_dir(),"time_trial"))


    get_times()
    get_best_time()

    for obj in sce.objects:
        if "Block_Checkpoint" in obj.name:
            cp_data.append(obj)
            gD["time_trial"]["cp_count"] = len(cp_data)
    if G.DEBUG: print("AMOUNT CHECKPOINTS", len(cp_data))

    logic.ui["sys"].add_overlay(TimeTrialUI)

    logic.game.set_music_dir("time_trial")

    # In debug mode, print when game mode is ready
    if G.DEBUG: print(own.name + ": Game mode Time Trial has been set up.")

    own["Timer"] = 0


def controls():
    pass


