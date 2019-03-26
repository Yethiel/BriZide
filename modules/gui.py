import os
import math
from mathutils import Vector
from bge import logic, events
from modules import btk, sound, development, helpers

from modules import config, video, global_constants as G
from modules.helpers import clamp

kbd = logic.keyboard
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED


class UIManager():
    def __init__(self):
        self.focus = "menu"
        self.previous = None
        self.queue = []
        self.go = None  # Game object used to spawn ui elements

    def set_focus(self, element):
        self.previous = self.focus
        self.focus = element
        if G.DEBUG: print("Set focus to", element)

    def enqueue(self, command):
        self.queue.append(command)

    def restore_focus(self):
        self.set_focus(self.previous)


def setup():
    own = logic.getCurrentController().owner

    # The game object that's used to spawn the UI (addObj)
    logic.uim.go = own

    # Dictionary for the UI layouts
    logic.ui = {}

    # Main menu layout
    layout = logic.ui["layout_main"] = btk.Layout("layout_main", logic.uim.go)

    logic.ui["label_level"] = btk.Label(layout, "LEVEL: {}".format(logic.settings["Game"]["leveldir"]), position=[8.55, 8.5, 0], size=0.3)
    logic.ui["label_level"].set_color((.5, .5, .5, 1.0))

    logic.ui["label_ship"] = btk.Label(layout, "SHIP: {}".format(logic.settings["Player"]["ship"]), position=[8.55, 8.1, 0], size=0.3)
    logic.ui["label_ship"].set_color((.5, .5, .5, 1.0))

    logic.ui["label_mode"] = btk.Label(layout, "MODE: {}".format(logic.settings["Game"]["mode"]), position=[8.55, 7.7, 0], size=0.3)
    logic.ui["label_mode"].set_color((.5, .5, .5, 1.0))

    logic.ui["label_best"] = btk.Label(layout, "BEST: ", position=[8.55, 7.3, 0], size=0.3)
    logic.ui["label_best"].set_color((.5, .5, .5, 1.0))
    update_best_time()

    menu = btk.Menu("menu_main", layout)
    menu.focus()

    # loads ship previews
    for folder in os.listdir(G.PATH_SHIPS):
        if folder+".inf" in os.listdir(logic.expandPath(G.PATH_SHIPS+folder)):
            print("LOADING", os.path.join(logic.expandPath(G.PATH_SHIPS+folder), folder) + ".blend")
            # logic.LibLoad(os.path.join(logic.expandPath(G.PATH_SHIPS+folder), folder) + ".blend", "Mesh")
            logic.LibNew("ui_"+os.path.join(logic.expandPath(G.PATH_SHIPS+folder), folder) + ".blend", "Mesh", [folder])

    # Debug menu
    menu_debug = btk.Menu("menu_debug", layout)
    menu_debug.populate(
        texts=[
            "[< Back]",
            "Start Editor",
            "Dump scenes to terminal",
            "Prepare for release and quit"
        ],
        position=[0.5, 4.0, 0],
        size=0.5,
        actions=[back, start_editor, dump_scenes, options_clean_files],
        hidden=True
    )
            
    # Main menu
    menu.populate(
        texts=[
            "Enter Name" if logic.settings["Player"]["name"] == "Player 0" else logic.settings["Player"]["name"],
            "Start Game",
            "Select Level",
            "Select Ship",
            "Select Game Mode",
            "Options",
            "Quit"
        ]+(["DEBUG"] if G.DEBUG else []),
        position=[0.5, 4.0, 0],
        size=0.5,
        actions=[
            enter_name,
            start_game,
            show_menu_level,
            show_menu_ship,
            show_menu_mode,
            show_menu_options,
            end_game
        ]+([show_menu_debug] if G.DEBUG else []),
        updates=[
            update_name,
            None,
            None,
            None,
            None,
            None,
            None
        ]+([None] if G.DEBUG else []),
        hidden=False
    )

    # Selects Start Game if a name has been entered
    if logic.settings["Player"]["name"] != "Player 0":
        menu.active = 1

    # Sub-menu: level selection
    menu_level = btk.Menu("menu_level", layout, select_callback=select_callback_level)
    menu_level.populate(
        texts=logic.game.level_list,
        position=[0.5, 4.0, 0],
        size=0.5,
        actions=[select_level for x in range(len(logic.game.level_list))],
        hidden=True
    )
    menu_level.set_active(logic.game.level_name)

    # Sub-menu: ship selection
    menu_ship = btk.Menu("menu_ship", layout)
    menu_ship.populate(
        texts=logic.game.ship_list,
        position=[0.5, 4.0, 0],
        size=0.5,
        actions=[select_ship for x in range(len(logic.game.ship_list))],
        hidden=True
    )
    # ship preview model
    menu_ship.set_active(logic.settings["Player"]["ship"])
    ship_preview = btk.Element(
        layout,
        object="ui_ship_preview",
        position=[13,4.0,0],
        scale=[1.0,1.0,1.0],
        title="ui_ship_preview",
        update=update_ship_preview,
        hidden=False
    )

    # Sub-menu: game mode
    menu_mode = btk.Menu("menu_mode", layout)
    menu_mode.populate(
        texts=["[< Back]"]+logic.game.mode_list,
        position=[0.5, 4.0, 0],
        size=0.5,
        actions=[back]+[select_mode for x in range(len(logic.game.mode_list))],
        hidden=True
    )
    menu_mode.set_active(logic.game.mode)

    # Sub-menu: game options
    bool_options = [
           "{}: {}".format("Fullscreen", logic.settings["Video"]["fullscreen"]),
           "{}: {}".format("Detailed Level Cube", logic.settings["Video"]["detailed_cube"]),
           "{}: {}".format("Bloom", logic.settings["Video"]["bloom"]),
           "{}: {}".format("Blur", logic.settings["Video"]["blur"]),
           "{}: {}".format("Lights", logic.settings["Video"]["lights"]),
           "{}: {}".format("Extra Textures", logic.settings["Video"]["extra_textures"]),
    ]
    menu_options = btk.Menu("menu_options", layout)
    menu_options.populate(
        texts=["[< Back]"]+bool_options,
        position=[0.5, 4.0, 0],
        size=0.5,
        actions=[back]+[set_option for x in range(len(bool_options))],
        hidden=True
    )

    # Misc. menu items
    logo = btk.Element(layout, object="logo", title="logo", position=[0.5, 6.5, 0.2], scale=[2,2,1])
    backdrop = btk.Element(layout, object="ui_menu_backdrop", title="backdrop", position=[0, 0, -3], scale=[1,1,1])
    title = btk.Label(layout, text="B r i Z i d e", position=[3, 7.3, 0.2], size=0.6, update=update_fade)
    title.set_color([1, 0.5, 0.0, 1.0])

    # Creates the loading screen
    layout_loading = logic.ui["loading_screen"] = btk.Layout("loading_screen", logic.uim.go)

    # "Loading"
    loading = btk.Label(layout_loading, text="Loading", position=[6.5, 3, 0.3], size=0.6, hidden=True, update=update_pulsate)

    # Displays the component that's being loaded
    loading_what = btk.Label(layout_loading, text="", position=[1, 1.15, 0.4], size=0.3, hidden=True, update=update_loading_label)
    loading_what.set_color([1, 1, 1, 1])

    loading_bar = btk.ProgressBar(layout_loading,
        position=[0, 1, 0.3],
        hidden=True,
        min_scale=[0, .5, 1],
        max_scale=[16, .5, 1],
        update=update_loading_bar
    )

    # Loading screen backdrop
    loading_screen = btk.Element(layout_loading, object="loading_screen", title="loading_screen", position=[0, 0, 0.1], hidden=True)


def update_fade(widget):
    widget.go.color[3] = clamp(logic.uim.go["timer"], 0.0, 1.0)


def update_pulsate(widget):
    c = math.sin(logic.uim.go["timer"]*8) / 4
    widget.set_color([0.75 + c, 0.75 + c, 0.65 + c, 1.0])


def update_loading_bar(widget):
    widget.progress = logic.components.get_percent()


def update_loading_label(widget):
    widget.text = logic.components.get_currently_loading()


def select_callback_level(widget):
    selection = logic.ui["layout_main"].get_element("menu_level").get_active().text
    logic.game.set_level(selection)
    logic.ui["label_level"].text = "LEVEL: {}".format(selection)
    update_best_time()


def update_ship_preview(widget):
    widget.go.localPosition.z = widget.go.localPosition.z + (math.sin(logic.uim.go["timer"]*1.5) * 0.007)
    widget.go.localOrientation *= Vector([(math.sin(logic.uim.go["timer"]*1.7) * 0.02), (math.sin(logic.uim.go["timer"]*1.5) * 0.02), 0])
    widget.go.applyRotation([1.3, 0.6, 3.0], False)

    selection = logic.ui["layout_main"].get_element("menu_ship").get_active()
    if selection:
        selected_ship = selection.text
    else:
        return
    if not selected_ship in [m.name for m in widget.go.meshes]:
        try:
            widget.go.replaceMesh(selected_ship, True, False)
        except:
            pass


def show_menu_options(widget):
    logic.ui["layout_main"].get_element("menu_options").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_main").hide()
    logic.ui["layout_main"].get_element("menu_options").focus()


def show_menu_level(widget):
    logic.ui["layout_main"].get_element("menu_level").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_main").hide()
    logic.ui["layout_main"].get_element("menu_level").focus()


def show_menu_ship(widget):
    logic.ui["layout_main"].get_element("menu_ship").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_main").hide()
    logic.ui["layout_main"].get_element("menu_ship").focus()


def show_menu_mode(widget):
    logic.ui["layout_main"].get_element("menu_mode").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_main").hide()
    logic.ui["layout_main"].get_element("menu_mode").focus()


def show_menu_debug(widget):
    logic.ui["layout_main"].get_element("menu_debug").show()
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.ui["layout_main"].get_element("menu_main").hide()
    logic.ui["layout_main"].get_element("menu_debug").focus()


def set_option(widget):
    if "Bloom" in widget.text:
        logic.settings["Video"]["bloom"] = config.setting_toggled(logic.settings["Video"]["bloom"])
        widget.text = "{}: {}".format(widget.text.split(':')[0], logic.settings["Video"]["bloom"])
    if "Blur" in widget.text:
        logic.settings["Video"]["blur"] = config.setting_toggled(logic.settings["Video"]["blur"])
        widget.text = "{}: {}".format(widget.text.split(':')[0], logic.settings["Video"]["blur"])
    if "Fullscreen" in widget.text:
        logic.settings["Video"]["fullscreen"] = config.setting_toggled(logic.settings["Video"]["fullscreen"])
        widget.text = "{}: {}".format(widget.text.split(':')[0], logic.settings["Video"]["fullscreen"])
    if "Detailed Level Cube" in widget.text:
        logic.settings["Video"]["detailed_cube"] = config.setting_toggled(logic.settings["Video"]["detailed_cube"])
        widget.text = "{}: {}".format(widget.text.split(':')[0], logic.settings["Video"]["detailed_cube"])
    if "Lights" in widget.text:
        logic.settings["Video"]["lights"] = config.setting_toggled(logic.settings["Video"]["lights"])
        widget.text = "{}: {}".format(widget.text.split(':')[0], logic.settings["Video"]["lights"])
    if "Extra Textures" in widget.text:
        logic.settings["Video"]["extra_textures"] = config.setting_toggled(logic.settings["Video"]["extra_textures"])
        widget.text = "{}: {}".format(widget.text.split(':')[0], logic.settings["Video"]["extra_textures"])
    logic.game.save_settings()


def enter_name(widget):
    logic.uim.go["ui_timer"] = 0.0
    logic.ui["layout_main"].get_element("menu_main").unfocus()
    logic.uim.go["log_keyboard"] = True
    logic.uim.go["keyboard"] = ""


def update_name(widget):
    if logic.uim.go["log_keyboard"] == True:
        widget.text = logic.uim.go["keyboard"] + ('|' if int(logic.uim.go["ui_timer"]*2) % 2 else "")
        if kbd.events[events.ENTERKEY] == JUST_ACTIVATED and logic.uim.go["ui_timer"] > 0.1:
            sound.play("select")
            logic.uim.go["log_keyboard"] = False
            player_name = logic.uim.go["keyboard"].strip()
            widget.text = player_name
            if player_name == "":
                player_name = "Player 0"
                widget.text = "Enter Name"
            logic.settings["Player"]["name"] = player_name
            logic.game.save_settings()
            logic.ui["layout_main"].get_element("menu_main").focus()
            update_best_time()


def options_clean_files(widget):
    development.clean_files()
    logic.endGame()

def back(widget):
    logic.game.save_settings()
    menu_id = widget.parent.title

    # to apply all gfx settings
    if menu_id == "menu_options":
        logic.restartGame()

    logic.ui["layout_main"].get_element(menu_id).unfocus()
    logic.ui["layout_main"].get_element("menu_main").focus()
    logic.ui["layout_main"].get_element("menu_main").show()
    logic.ui["layout_main"].get_element(menu_id).hide()


def update_best_time():
    if logic.game.mode != "time_trial":
        logic.ui["label_best"].text = ""
        return
    best_time = logic.game.get_best_time()
    if best_time["player"] == "":
        logic.ui["label_best"].text = "NO BEST TIME YET"
    else:
        logic.ui["label_best"].text  = "BEST: {} ({})".format(
            helpers.time_string(best_time["time"]),
            best_time["player"]
        )
    if best_time["player"] == logic.settings["Player"]["name"]:
        logic.ui["label_best"].set_color((.1, .9, .1, 1.0))
    else:
        logic.ui["label_best"].set_color((.9, .1, .1, 1.0))



def select_level(widget):
    logic.game.set_level(widget.text)
    logic.ui["label_level"].text = "LEVEL: {}".format(widget.text)
    update_best_time()
    logic.game.save_settings()
    logic.ui["layout_main"].get_element("menu_level").unfocus()
    logic.ui["layout_main"].get_element("menu_main").focus()
    logic.ui["layout_main"].get_element("menu_main").show()
    logic.ui["layout_main"].get_element("menu_level").hide()


def select_ship(widget):
    logic.game.set_ship(widget.text)
    logic.ui["label_ship"].text = "SHIP: {}".format(widget.text)
    logic.game.save_settings()
    logic.ui["layout_main"].get_element("menu_ship").unfocus()
    logic.ui["layout_main"].get_element("menu_main").focus()
    logic.ui["layout_main"].get_element("menu_main").show()
    logic.ui["layout_main"].get_element("menu_ship").hide()


def select_mode(widget):
    logic.game.set_mode(widget.text)
    logic.ui["label_mode"].text = "MODE: {}".format(widget.text)
    update_best_time()
    logic.game.save_settings()
    logic.ui["layout_main"].get_element("menu_mode").unfocus()
    logic.ui["layout_main"].get_element("menu_main").focus()
    logic.ui["layout_main"].get_element("menu_main").show()
    logic.ui["layout_main"].get_element("menu_mode").hide()


def start_game(widget):
    logic.game.save_settings()
    logic.ui["layout_main"].hide()
    logic.ui["loading_screen"].show()
    logic.ui["layout_main"].unfocus()
    logic.uim.enqueue("game_start")


def start_editor(widget):
    logic.game.set_mode("editor")
    logic.ui["layout_main"].hide()
    logic.ui["loading_screen"].show()
    logic.ui["layout_main"].unfocus()
    logic.uim.enqueue("game_start")


def dump_scenes(widget):
    development.dump_scenes()


def end_game(widget):
    logic.game.save_settings()
    logic.device.stopAll()
    logic.music_device.stopAll()
    logic.endGame()


def main():
    elements = logic.ui.copy().keys()
    for element in elements:
        if element in logic.ui:
            if not hasattr(logic.ui[element], "go") or logic.ui[element].go.visible:
                logic.ui[element].run()
