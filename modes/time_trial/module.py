import os
from mathutils import Color
from bge import logic, events
from modules import components, global_constants, sound, helpers, btk, lights
from modules import global_constants as G
from random import randint

required_components = ["blocks", "level", "cube", "ship"]
trigger_distance = 32 # distance for a checkpoint to be triggered
game = logic.game

kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

#         self.lbl_count = bgui.Label(
#             self.frame, 
#             text="1", 
#             pos=[0.5, 0.7], 
#             sub_theme='Large', 
#             options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX
#         )
#         self.lbl_checkpoints = bgui.Label(
#             self.frame, 
#             text="0/0", 
#             pos=[0.2, 0.85], 
#             options = bgui.BGUI_DEFAULT
#         )
#         self.lbl_time = bgui.Label(
#             self.frame, 
#             text="", 
#             pos=[0.5, 0.85], 
#             sub_theme='Large', 
#             options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX
#         )
#         self.lbl_best = bgui.Label(
#             self.frame, 
#             text="BEST: ",
#             pos=[0.5, 0.82], 
#             options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX
#         )

#         self.button_menu = bgui.FrameButton(self.frame,
#                 text="Back to Menu",
#                 size=[.2, .1],
#                 pos=[0.5, .3],
#                 options = bgui.BGUI_DEFAULT
#         )

#         self.button_menu.on_click = self.return_to_menu
#         self.button_menu.visible = False

#     def update(self):

#         own = self.cont_obj
#         tt = logic.time_trial
#         if own["done_loading"]:

#             self.lbl_best.text = "BEST: {} ({})".format(
#                 helpers.time_string(tt.best_time["time"]), 
#                 tt.best_time["player"]
#             )
#             self.lbl_checkpoints.text = "Chk " + str(tt.cp_progress[str(0)]) +"/"+ str(tt.cp_count)


#             if own["CountdownTimer"] > 4 and gD:
#                 if not tt.cp_count == tt.cp_progress["0"]:
#                     self.lbl_time.text = helpers.time_string(own["Timer"])

#             amnt_passed = tt.cp_progress["0"]
#             if amnt_passed == len(tt.cp_data):
#                 self.button_menu.visible = True
#             else:
#                 self.button_menu.visible = False    




class TimeTrial():
    def __init__(self, controller):
        self.cp_data = []
        self.cp_count = 0
        self.cp_progress = {"0": 0}
        self.best_times = []
        self.best_time = {"player": "", "time": 999.0}
        self.final_time = 0.0
        self.controller = logic.getCurrentController().owner

    def setup_checkpoints(self, sce):
        for obj in sce.objects:
            if "Block_Checkpoint" in obj.name:
                self.cp_data.append(obj)
        self.cp_count = len(self.cp_data)

    def get_times(self, game):
        # Gets the best times of all players
        for player in os.listdir(G.PATH_PROFILES):
            score_file = os.path.join(
                G.PATH_PROFILES, 
                player, 
                "time_trial", 
                "{}.txt".format(game.level_name)
            )

            if os.path.isfile(score_file):
                with open(score_file, "r") as f:
                    for line in f:
                        self.best_times.append(
                            {"player": player,
                             "time": float(line)}
                        )
            elif G.DEBUG:
                print(
                    "Times file does not exist for {}".format(game.level_name)
                )

        # Gets the best time
        for time in self.best_times:
            if time["time"] < self.best_time["time"]:
                self.best_time = time

    def write_time(self, game):
        tt_file_path = os.path.join(
            game.get_profile_dir("0"),
            "time_trial", 
            "{}.txt".format(game.level_name)
        )

        with open(tt_file_path, "a") as f:
            f.write(str(self.final_time) + '\n')

    def countdown(self, cont_obj):
        if cont_obj["countdown"] > -1 and cont_obj["CountdownTimer"] > 1:
            if cont_obj["countdown"] == 4:
                sound.play("three" + str(randint(0,4)))
                # sound.EchoWrapper("three0").play()
                cont_obj["countdown"] -= 1
            if cont_obj["countdown"] == 3 and cont_obj["CountdownTimer"] > 2:
                sound.play("two" + str(randint(0,4)))
                cont_obj["countdown"] -= 1
            if cont_obj["countdown"] == 2 and cont_obj["CountdownTimer"] > 3:
                sound.play("one" + str(randint(0,4)))
                cont_obj["countdown"] -= 1
            if cont_obj["countdown"] == 1 and cont_obj["CountdownTimer"] > 4:
                # sound.play("go" + str(randint(0,4)))
                sound.EchoWrapper("go" + str(randint(0,4))).play()
                cont_obj["countdown"] -= 1
                # Give controls to the player
                logic.uim.focus = "ship"
                cont_obj["Timer"] = 0.0
            if cont_obj["countdown"] == 0 and cont_obj["CountdownTimer"] > 5:
                cont_obj["countdown"] -= 1

    def checkpoints(self, game, cont_obj):
        for cp in self.cp_data:
            for ship in game.ships:

                if game.ships[ship].go.getDistanceTo(cp) <= trigger_distance:
                    if not str(ship) in cp:
                        cp[str(ship)] = True
                        sound.play("checkpoint")
                        if G.DEBUG: 
                            print("Ship", ship, "passed", self.cp_data.index(cp))

                        cp.color = [.05, .05, .0, 1]

                        cp.worldScale = [0.2, 0.2, 0.2]

                        amnt_passed = 0
                        for cp in self.cp_data:
                            if str(ship) in cp:
                                amnt_passed += 1
                        
                        if G.DEBUG: print(amnt_passed, "/", len(self.cp_data))
                        
                        self.cp_progress[str(ship)] = amnt_passed
                        if amnt_passed == len(self.cp_data):
                            logic.uim.set_focus("menu")

                            menu = logic.ui["time_trial"].get_element("pause_menu")
                            menu.show()
                            menu.focus()
                            logic.uim.set_focus("menu")
                            logic.time_trial.controller["ui_timer"] = 0

                            if G.DEBUG: print("Time Trial over.")

                            self.final_time = cont_obj["Timer"]
                            self.write_time(game)

                            sound.play("race_complete")


def update_label_speed(widget):
    ship = game.get_ship_by_player(0)
    if ship:
        # self.bar_boost.percent = ship.current_boost/500
        widget.text = ">>> " + str(int(ship.current_velocity))

def update_label_time(widget):
    own = logic.time_trial.controller
    tt = logic.time_trial
    if own["CountdownTimer"] > 4:
        if not tt.cp_count == tt.cp_progress["0"]:
            widget.text = helpers.time_string(own["Timer"])

def update_label_countdown(widget):
    own = logic.time_trial.controller

    if not "countdown" in own:
        own["countdown"] = 4
    if own["countdown"] < 4:
        widget.text = str(own["countdown"])
    else:
        widget.text = ""
    if own["countdown"] == 0:
        widget.text = "GO!"
    if own["countdown"] == -1:
        widget.text = ""


def update_label_checkpoints(widget):
    tt = logic.time_trial
    widget.text = "Chk " + str(tt.cp_progress[str(0)]) +"/"+ str(tt.cp_count)

def update_checkpoint_bar(widget):
    tt = logic.time_trial
    if tt.cp_count != 0:
        widget.progress = tt.cp_progress[str(0)] / tt.cp_count

def update_boost_bar(widget):
    ship = logic.game.get_ship_by_player(0)
    if ship:
        widget.progress = ship.current_boost/500

def update_label_best(widget):
    tt = logic.time_trial
    widget.text  = "BEST: {} ({})".format(
            helpers.time_string(tt.best_time["time"]), 
            tt.best_time["player"]
    )


def return_to_menu(widget):
    sce = logic.getCurrentScene()
    own = logic.time_trial.controller

    logic.ui["time_trial"].end()
    logic.ui.pop("time_trial")

    for component in required_components:
        logic.components.free(component)
    own.endObject()

    logic.components.free("time_trial")
    logic.components.clear()
    logic.game.clear()
    logic.uim.set_focus("menu")
    logic.game.set_music_dir("menu")

    logic.ui["layout_main"].get_element("menu_main").show()
    logic.ui["layout_main"].get_element("logo").show()
    logic.ui["layout_main"].get_element("B r i Z i d e").show()
    logic.ui["layout_main"].get_element("menu_main").focus()


def restart(widget):
    sce = logic.getCurrentScene()
    own = logic.time_trial.controller

    logic.ui["time_trial"].end()
    logic.ui.pop("time_trial")
    logic.ui["layout_loading"].show()

    for component in required_components:
        logic.components.free(component)
    own.endObject()

    logic.components.free("time_trial")
    logic.components.clear()
    logic.game.clear()
    logic.uim.set_focus("menu")
    
    logic.uim.enqueue("game_start")


def init():
    """ Runs once before or while loading """

    own = logic.getCurrentController().owner

    logic.components = components.Components()
    logic.time_trial = TimeTrial(own)
    queue_id = logic.components.enqueue(required_components)

    sce = logic.getCurrentScene()

    own["init"] = True

    # Creates a new BTK layout for the HUD
    logic.ui["time_trial"] = btk.Layout("time_trial", logic.uim.go)
    layout = logic.ui["time_trial"]

    btk.Label(layout, text="", position=[7.5, 7.5, 0], size=1.0, update=update_label_countdown)

    btk.Label(layout, text="", position=[0.5, 7.5, 0], size=0.6, update=update_label_time)
    btk.Label(layout, text="", position=[0.52, 7.2, 0], size=0.2, update=update_label_best)
    btk.Label(layout, text="", position=[0.5, 6.5, 0], size=0.4, update=update_label_checkpoints)

    btk.Label(layout, text="", position=[12, 0.5, 0], size=0.6, update=update_label_speed)    

    boost_bar = btk.ProgressBar(
        layout, 
        title="boost", 
        position=[0.5, 0.5, 0], 
        min_scale=[0, .5, 1], 
        max_scale=[4, .5, 1], 
        update=update_boost_bar
    )
    boost_bar.set_color([1, .743, 0.0, 0.75])

    checkpoint_bar = btk.ProgressBar(
        layout, 
        title="checkpoints_bar", 
        position=[0.5, 6.45, -0.1], 
        min_scale=[0, .4, 1], 
        max_scale=[2.5, .4, 1], 
        update=update_checkpoint_bar
    )
    checkpoint_bar.set_color([1, .743, 0.0, 0.75])


    # Creates a pause menu and populates it with options
    menu = btk.Menu("pause_menu", layout)
    menu.populate(
        texts=[
            "Restart", 
            "Return to Menu"
        ], 
        position=[0.5, 5.0, 0],
        size=0.5,
        actions=[
            restart,
            return_to_menu
        ],
        hidden=False
    )
    
    menu.hide()


def load(cont_obj):
    # Prepare the game mode by loading the queued components
    logic.components.load()

    # If the queue is emtpy we're done
    if logic.components.is_done(required_components):
        cont_obj["done_loading"] = True
        setup()


def main():
    """ Runs every logic tick """
    sce = logic.getCurrentScene()
    own = logic.getCurrentController().owner   
    game = logic.game

    if own["init"]:

        if not own["done_loading"]:
            load(own)

    tt = logic.time_trial

    tt.countdown(own)
    tt.checkpoints(game, own)
    
    # Controls the pause menu
    menu = logic.ui["time_trial"].get_element("pause_menu")
    if own["ui_timer"] > 0.01:
        if logic.uim.focus == "ship" and kbd.events[events.ESCKEY] == JUST_ACTIVATED:
            menu.show()
            menu.focus()
            logic.uim.set_focus("menu")
            own["ui_timer"] = 0
        elif logic.uim.focus == "menu" and kbd.events[events.ESCKEY] == JUST_ACTIVATED:
            menu.hide()
            menu.unfocus()
            logic.uim.set_focus("ship")
            own["ui_timer"] = 0


def setup():
    """ Runs when loading is done """

    sce = logic.getCurrentScene()
    own = logic.getCurrentController().owner
    game = logic.game

    logic.ui["layout_loading"].hide()

    # Creates a folder for the mode
    if not os.path.isdir(os.path.join(game.get_profile_dir("0"),"time_trial")):
        os.makedirs(os.path.join(game.get_profile_dir("0"),"time_trial"))


    tt = logic.time_trial

    tt.setup_checkpoints(sce)
    tt.get_times(game)
    game.set_music_dir("time_trial")
    logic.uim.set_focus("")

    if G.DEBUG: print(own.name + ": Game mode Time Trial has been set up.")

    own["Timer"] = 0