import sys

import bgui
import bgui.bge_utils
from bge import logic

from modules import menu

globalDict = logic.globalDict


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
class MainMenu(bgui.bge_utils.Layout):

    def __init__(self, sys, data):
        super().__init__(sys, data)

        self.menu = menu.Menu()

        list = menu.List(label="Game Mode")

        for game_mode in logic.game.mode_list:
            list.options.append(menu.Option(game_mode, game_mode, None))

        self.menu.options.append(menu.Option("Start game", "start_game", self.start))

        self.menu.guilabels = []

        # Use a frame to store all of our widgets
        self.frame = bgui.Frame(self, border=0)
        self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

        pos = 0.0
        for option in self.menu.options:
            self.menuthing = bgui.Label(self.frame, text=option.label, pos=[0.1, pos], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
            self.menu.guilabels.append(bgui.Label(self.frame, text=option.label, pos=[0.5, pos], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED))
            pos -= .2


        # A themed frame
        self.win = bgui.Frame(self, size=[0.8, 0.8],
            options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
        self.win.colors = [(0, 0, 0, 0) for i in range(4)]


        # Create an image to display
        self.win.img = bgui.Image(self.frame, '//gfx/title.png', pos=[0, 0],
            options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED|bgui.BGUI_CACHE)

        # for x in range(0, len(logic.game.mode_list)):
        #     setattr(self, "x")
        self.mode_buttons = []
        amnt_modes = len(logic.game.mode_list)

        # add all game modes to the menu (tab-style)
        for x in range(0, amnt_modes):

            button = bgui.FrameButton(self.win,
                text=logic.game.mode_list[x],
                size=[1/amnt_modes, .1],
                pos=[x/amnt_modes, .9],
                options = bgui.BGUI_DEFAULT)

            button.on_click = self.select_mode
            self.mode_buttons.append(button)

        self.button_start = bgui.FrameButton(self.win, text='Start', size=[.14, .1], pos=[.815, .03],
            options = bgui.BGUI_DEFAULT)
        self.button_start.on_click = self.start

    def select_mode(self,widget):
        logic.game.set_mode(widget.text)

    def start(self, widget):
        logic.ui["sys"].remove_overlay(MainMenu)
        logic.game.start()
