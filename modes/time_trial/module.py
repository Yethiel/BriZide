import os
from bge import logic, events, render
from modules import btk, cube, components, sound, helpers, global_constants as G
from modules.game_mode import Game_Mode
from random import randint

required_components = ["blocks", "level", "cube", "ship"]

trigger_distance = 32 # distance for a checkpoint to be triggered

class Time_Trial_Mode(Game_Mode):
    def __init__(self, game_obj):
        # initiates the game mode, name needs to match folder name
        super().__init__(required_components, game_obj, "time_trial")
        self.cp_data = []
        self.cp_count = 0
        self.cp_progress = {"0": 0}
        self.best_times = []
        self.best_time = {"player": "", "time": 9999.0}
        self.final_time = 0.0
        # adds additional menu entries to the pause menu
        game = logic.game
        index_current_level = game.level_list.index(game.level_name)
        if index_current_level+1 < len(game.level_list):
            next_level_string = "Next Level: {}".format(game.level_list[index_current_level+1])
        else:
            next_level_string = "Start over with first level: {}".format(game.level_list[0])
        self.menu_texts = ["Start over [BACKSPACE]", next_level_string]#, "Restart Mode"]
        self.menu_actions = [self.start_over, self.next_level]#, self.restart]

    def setup(self):
        """ Runs after loading is done """
        super().setup()  # generates the UI layout and menu
        sce = logic.getCurrentScene()
        logic.game.set_music_dir("time_trial")
        self.setup_checkpoints()
        self.get_times()

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

        logic.game.ships[0].current_boost = 500

    def run(self):
        """ runs every logic tick """
        super().run()  # handles loading of components

        self.countdown()
        self.checkpoints()

        if helpers.keystat("BACKSPACEKEY", "JUST_RELEASED"):
            self.start_over(None)

    def start_over(self, widget):
        """ Callback for Start Over menu entry """
        self.mode_done = False
        logic.ui[self.name].get_element("pause_menu").unfocus()
        logic.ui[self.name].get_element("pause_menu").hide()
        self.setup_checkpoints()
        self.get_times()
        logic.uim.set_focus("time_trial")
        ship = helpers.get_scene("Scene").objects["Ship"]
        ship.worldPosition = logic.game.level.get_start_pos()
        ship.worldOrientation = logic.game.level.get_start_orientation()
        ship.linearVelocity = [0, 0, 0]
        self.final_time = 0.0
        self.go["countdown"] = 4
        self.go["CountdownTimer"] = 0.0
        logic.game.ships[0].gravity = 0 if logic.game.get_level().cube_size == 0 else 150
        logic.game.ships[0].current_boost = 500

    def next_level(self, widget):
        game = logic.game
        self.mode_done = False
        index_current_level = game.level_list.index(game.level_name)
        if index_current_level + 1 < len(game.level_list):
            if index_current_level + 2 < len(game.level_list):
                widget.text = "Next level: {}".format(game.level_list[index_current_level+2])
            else:
                widget.text = "Start over with first level: {}".format(game.level_list[0])
            next_level = game.level_list[index_current_level+1]
        else:
            next_level = game.level_list[0]
            widget.text = "Next level: {}".format(game.level_list[1])
        game.level.clear()
        cube.clear()
        game.set_level(next_level)
        logic.game.save_settings()
        game.level.set_identifier(next_level)
        game.level.load()
        if G.DEBUG: game.level.print_info()
        game.level.place()
        cube.main()
        self.start_over(None)

    def setup_checkpoints(self):
        self.cp_count = 0
        self.cp_progress = {"0": 0}
        self.cp_data = []
        sce = helpers.get_scene("Scene")
        for obj in sce.objects:
            if "Block_Checkpoint" in obj.name and not "end" in obj:
                obj["0"] = False
                obj.color = [1.0, 1.0, 1.0, 1]
                obj.worldScale = [1.0, 1.0, 1.0]
                self.cp_data.append(obj)
        self.cp_count = len(self.cp_data)

    def get_times(self):
        # Gets the best times of all players
        for player in os.listdir(G.PATH_PROFILES):
            if player == ".gitkeep":
                continue
            score_file = os.path.join(
                G.PATH_PROFILES,
                player,
                "time_trial",
                "{}.txt".format(logic.game.level_name)
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
                    "Times file does not exist for {} ({})".format(logic.game.level_name, score_file)
                )

        # Gets the best time
        for time in self.best_times:
            if time["time"] < self.best_time["time"]:
                self.best_time = time

    def write_time(self):
        tt_file_path = os.path.join(
            logic.game.get_profile_dir("0"),
            "time_trial",
            "{}.txt".format(logic.game.level_name)
        )

        with open(tt_file_path, "a") as f:
            f.write(str(self.final_time) + '\n')

    def countdown(self):
        if self.go["countdown"] > -1 and self.go["CountdownTimer"] > 1:
            if self.go["countdown"] == 4:
                sound.play("three" + str(randint(0,4)))
                # sound.EchoWrapper("three0").play()
                self.go["countdown"] -= 1
            if self.go["countdown"] == 3 and self.go["CountdownTimer"] > 2:
                sound.play("two" + str(randint(0,4)))
                self.go["countdown"] -= 1
            if self.go["countdown"] == 2 and self.go["CountdownTimer"] > 3:
                sound.play("one" + str(randint(0,4)))
                self.go["countdown"] -= 1
            if self.go["countdown"] == 1 and self.go["CountdownTimer"] > 4:
                # sound.play("go" + str(randint(0,4)))
                sound.EchoWrapper("go" + str(randint(0,4))).play()
                self.go["countdown"] -= 1
                # Give controls to the player
                logic.uim.focus = "ship"
                self.go["Timer"] = 0.0
            if self.go["countdown"] == 0 and self.go["CountdownTimer"] > 5:
                self.go["countdown"] -= 1

    def checkpoints(self):
        for cp in self.cp_data:
            for ship in logic.game.ships:
                if logic.game.ships[ship].go.getDistanceTo(cp) <= trigger_distance:
                    if not cp["0"]:
                        cp[str(ship)] = True
                        sound.play("checkpoint")
                        if G.DEBUG:
                            print("Ship", ship, "passed", self.cp_data.index(cp))

                        cp.color = [.05, .05, .0, 1]
                        cp.worldScale = [0.2, 0.2, 0.2]

                        amnt_passed = 0
                        for cp in self.cp_data:
                            if cp["0"]:
                                amnt_passed += 1

                        if G.DEBUG: print(amnt_passed, "/", len(self.cp_data))

                        self.cp_progress[str(ship)] = amnt_passed
                        if amnt_passed == len(self.cp_data):
                            menu = logic.ui["time_trial"].get_element("pause_menu")
                            menu.show()
                            menu.focus()
                            self.mode_done = True
                            logic.uim.set_focus("menu")
                            self.go["ui_timer"] = 0

                            if G.DEBUG: print("Time Trial over.")

                            self.final_time = self.go["Timer"]
                            self.write_time()

                            sound.play("race_complete")


def update_label_speed(widget):
    ship = logic.game.get_ship_by_player(0)
    if ship:
        # self.bar_boost.percent = ship.current_boost/500
        widget.text = ">>> " + str(int(ship.current_velocity))

def update_label_time(widget):
    own = logic.time_trial.go
    tt = logic.time_trial
    if own["CountdownTimer"] > 4:
        if not tt.cp_count == tt.cp_progress["0"]:
            widget.text = helpers.time_string(own["Timer"])

def update_label_countdown(widget):
    own = logic.time_trial.go

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
    if tt.best_time["player"] == "":
        widget.text = "NO BEST TIME YET"
    else:
        widget.text  = "BEST: {} ({})".format(
            helpers.time_string(tt.best_time["time"]),
            tt.best_time["player"]
        )

def init():
    """ Runs immediately after the scene loaded """
    logic.time_trial = Time_Trial_Mode(logic.getCurrentController().owner)

    # Creates a folder for the mode
    if not os.path.isdir(os.path.join(logic.game.get_profile_dir("0"),"time_trial")):
        os.makedirs(os.path.join(logic.game.get_profile_dir("0"),"time_trial"))

def main():
    logic.time_trial.run()
