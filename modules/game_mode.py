from bge import logic, events
from modules import btk
from modules.helpers import get_scene
from modules import global_constants as G

kbd = logic.keyboard

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

class Game_Mode:
    """ Game mode object that handles loading of components """
    def __init__(self, components, game_obj, name="custom_mode"):
        """
            components: List of level components to load
            game_obj:   KX_GameObj that runs the module
            name:       Name of the game mode. Needs to match folder name
        """
        self.name = name
        self.queue_id = logic.components.enqueue(components)
        self.components = components
        self.loaded = False
        self.go = game_obj

    def setup(self):
        """ Runs once all components have been loaded """
        logic.ui[self.name] = btk.Layout(self.name, logic.uim.go)

        # Creates a pause menu and populates it with options
        menu = btk.Menu("pause_menu", logic.ui[self.name])
        menu.populate(
            texts=[
                "Restart", 
                "Return to Menu"
            ], 
            position=[0.5, 5.0, 0],
            size=0.5,
            actions=[
                self.restart,
                self.return_to_menu
            ]
        )
        menu.hide()
        logic.uim.set_focus(self.name)


    def run(self):
        """ Runs every logic tick """
        
        if not self.loaded:
            if G.DEBUG: print("Not loaded yet.")
            # Prepares the game mode by loading the queued components
            logic.components.load()

            # Loading is done, runs setup function
            if logic.components.is_done(self.components):
                self.loaded = True
                self.setup()
                logic.ui["loading_screen"].hide()
            return

        menu = logic.ui[self.name].get_element("pause_menu")
        if logic.uim.go["ui_timer"] > 0.01:
            if logic.uim.focus != "menu" and kbd.events[events.ESCKEY] == JUST_ACTIVATED:
                menu.show()
                menu.focus()
                logic.uim.set_focus("menu")
                logic.uim.go["ui_timer"] = 0
            elif logic.uim.focus == "menu" and kbd.events[events.ESCKEY] == JUST_ACTIVATED:
                menu.hide()
                menu.unfocus()
                logic.uim.restore_focus()
                logic.uim.go["ui_timer"] = 0


    def return_to_menu(self, widget):
        # sce = logic.getCurrentScene()

        # logic.ui[self.name].hide()
        # logic.ui[self.name].end()
        # logic.ui.pop(self.name)

        # for component in self.components[::-1]:
        #     logic.components.free(component)
        # self.go.endObject()

        # logic.components.free(self.name)
        # logic.components.clear()
        # logic.game.clear()
        # logic.uim.set_focus("menu")
        # logic.game.set_music_dir("menu")

        # logic.ui["layout_main"].get_element("menu_main").show()
        # logic.ui["layout_main"].get_element("logo").show()
        # logic.ui["layout_main"].get_element("B r i Z i d e").show()
        # logic.ui["layout_main"].get_element("menu_main").focus()


        # if G.DEBUG:
        #     from modules import debug
        #     debug.dump_scenes()

        # Workaround: BGE LibLoad-related crash
        logic.restartGame()


    def restart(self, widget):
        logic.device.stopAll()  # stops all sounds
        sce = logic.getCurrentScene()
        if G.DEBUG: print("Ending UI")
        logic.ui[self.name].end()
        if G.DEBUG: print("Popping UI")
        logic.ui.pop(self.name)
        if G.DEBUG: print("Showing loading screen")
        logic.ui["loading_screen"].show()

        for component in self.components[::-1]:
            logic.components.free(component)
        if G.DEBUG: print("Ending controller object")
        self.go.endObject()

        if G.DEBUG: print("Freeing own component")
        logic.components.free(self.name)
        logic.components.clear()
        logic.game.clear()
        logic.uim.set_focus("menu")
        
        logic.uim.enqueue("game_start")
