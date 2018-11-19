import sys

import bgui
import bgui.bge_utils
from bge import logic

from modules.editor_ops import delete_block
from modules import global_constants as G
gD = logic.globalDict

own = logic.getCurrentController().owner


class ListBoxRenderer():
    """Base class for rendering an item in a ListBox"""
    def __init__(self, listbox):
        """
        :param listbox: the listbox the renderer will be used with (used for parenting)
        """
        self.label = bgui.Label(listbox, "label")

    def render_item(self, item):
        """Creates and returns a :py:class:`bgui.label.Label` representation of the supplied item

        :param item: the item to be rendered
        :rtype: :py:class:`bgui.label.Label`
        """
        self.label.text = str(item)


        return self.label
class EditorUI(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)

        FRAME_PROP_WIDTH = .18
        FRAME_PROP_HEIGHT = 1
        FRAME_PROP_PADDING_TOP = 0.02

        FRAME_MENU_HEIGHT = 0.03

        self.focus_before = "editor_main"

        self.main = bgui.Frame(self, border=0)
        self.main.colors = [(0, 0, 0, 0) for i in range(4)]


        # menu bar
        self.frame_menu = bgui.Frame(
            self.main,
            size=[1, FRAME_MENU_HEIGHT],
            pos=[0, 1-FRAME_MENU_HEIGHT],
            sub_theme="menu_bar",
            options=bgui.BGUI_DEFAULT)
        self.frame_menu.on_hover=self.set_focus_ui
        self.frame_menu.on_mouse_exit=self.lift_focus_ui

        self.button_file = bgui.FrameButton(
            self.frame_menu,
            text="File",
            size=[0.1, 1],
            pos=[0, 0],
            sub_theme="menu_bar",
            options = bgui.BGUI_DEFAULT)
        self.button_file.pt_size = 18

        self.level_name = bgui.TextInput(
            self.frame_menu,
            text="UNSET",
            size=[0.3, 1],
            pos=[0.1, 0],
            options = bgui.BGUI_DEFAULT
        )

        # Block property panel
        self.frame_prop = bgui.Frame(
            self.main,
            size=[FRAME_PROP_WIDTH, FRAME_PROP_HEIGHT],
            pos=[1-FRAME_PROP_WIDTH, -FRAME_MENU_HEIGHT],
            options=bgui.BGUI_DEFAULT)

        self.frame_prop.on_hover=self.set_focus_ui
        self.frame_prop.on_mouse_exit=self.lift_focus_ui
        self.frame_prop.colors = [(0.2, 0.2, 0.2, 0.8) for i in range(4)]

        self.frame_prop.label_active_block = bgui.TextInput(self.frame_prop, text="Block Name",
            size=[0.9, .04],
            pos=[0, 1-.04-FRAME_PROP_PADDING_TOP],
            input_options = bgui.BGUI_INPUT_SELECT_ALL, options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

        self.frame_prop.button_delete = bgui.FrameButton(
            self.frame_prop, text="Delete",
            size=[0.9, .04],
            pos=[0, 1-.08-FRAME_PROP_PADDING_TOP],
            options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
        self.frame_prop.button_delete.on_click = delete_block

    def set_focus_ui(self, widget):
        if logic.uim.focus != G.FOCUS_UI and not G.FOCUS_LOCK:
            if G.DEBUG: print(own.name, "Set focus to UI")
            self.focus_before = logic.uim.focus
        logic.uim.set_focus(G.FOCUS_UI)
    
    def lift_focus_ui(self,widget):
        if not G.FOCUS_LOCK:
            if G.DEBUG: print(own.name, "Lifted focus from UI")
            logic.uim.set_focus(self.focus_before)
   
    def update(self):
        try: self.frame_prop.label_active_block.text = gD["editor"]["active_block"].name
        except: self.frame_prop.label_active_block.text = "Nothing selected."

        if logic.game.level is not None:
            if self.level_name.text == "UNSET":
                self.level_name.text = logic.game.level.identifier
            else:
                logic.game.level.set_identifier(self.level_name.text)

    def lb_modes_click(self, widget):
        gD["settings"]["Game"]["mode"] = widget.selected

    def select_mode(self,widget):
        gD["settings"]["Game"]["mode"] = widget.text

    def start(self, widget):
        logic.sendMessage("start", gD["settings"]["Game"]["mode"])
        gD[G.FOCUS_UI]["sys"].remove_overlay(EditorUI)
