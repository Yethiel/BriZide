import sys

import bgui
import bgui.bge_utils
from bge import logic

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

		# Use a frame to store all of our widgets
		self.frame = bgui.Frame(self, border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

		# A themed frame
		self.win = bgui.Frame(self, size=[0.8, 0.8],
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.win.colors = [(0, 0, 0, 0) for i in range(4)]


		# Create an image to display
		self.win.img = bgui.Image(self.frame, '//gfx/title.bmp', pos=[0, 0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED|bgui.BGUI_CACHE)

		# self.lb_modes = bgui.ListBox(self.win, "lb_modes", items=globalDict["content"]["modes"], padding=0.05, size=[0.09, 0.09], pos=[.04, 0.1])
		# self.lb_modes.renderer = ListBoxRenderer(self.lb_modes)
		# self.lb_modes.on_click = self.lb_modes_click

		# for x in range(0, len(globalDict["content"]["modes"])):
		# 	setattr(self, "x")

		self.button = bgui.FrameButton(self.win, text=globalDict["content"]["modes"][0], size=[.5, .1], pos=[0, .9],
			options = bgui.BGUI_DEFAULT)
		self.button.on_click = self.select_mode

		self.button = bgui.FrameButton(self.win, text=globalDict["content"]["modes"][1], size=[.5, .1], pos=[.5, .9],
			options = bgui.BGUI_DEFAULT)
		self.button.on_click = self.select_mode
		
		self.button = bgui.FrameButton(self.win, text='Start', size=[.14, .1], pos=[.815, .03],
			options = bgui.BGUI_DEFAULT)
		self.button.on_click = self.start

	def lb_modes_click(self, widget):
		globalDict["settings"]["Game"]["mode"] = widget.selected

	def select_mode(self,widget):
		globalDict["settings"]["Game"]["mode"] = widget.text

	def start(self, widget):
		logic.sendMessage("start", globalDict["settings"]["Game"]["mode"])
		globalDict["ui"]["sys"].remove_overlay(MainMenu)
