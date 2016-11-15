import sys
import bgui
import bgui.bge_utils
from bge import logic
from scripts.ui_main_menu import MainMenu
from scripts import global_constants as G


globalDict = logic.globalDict

class MainUI(bgui.bge_utils.Layout):
	def __init__(self, sys, data):
		super().__init__(sys, data)


# This is the topmost overlay for debug stuff
class OverlayUI(bgui.bge_utils.Layout):
	def __init__(self, sys, data):
		super().__init__(sys, data)
		self.frame = bgui.Frame(self, border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

		self.lbl_fps = bgui.Label(self.frame, text="fps", pos=[0.1, 0.9], options = bgui.BGUI_DEFAULT)
		self.lbl_tck = bgui.Label(self.frame, text="tck", pos=[0.1, 0.85], options = bgui.BGUI_DEFAULT)
		self.lbl_rev = bgui.Label(self.frame, text="Brizide rev. " + G.REVISION, pos=[0.1, 0.1], options = bgui.BGUI_DEFAULT)

	def update(self):
		self.lbl_fps.text = str(int(logic.getAverageFrameRate()))
		self.lbl_tck.text = str(int(logic.getLogicTicRate()))

def main(cont):
	own = cont.owner
	mouse = logic.mouse

	if 'sys' not in globalDict["ui"]:
		globalDict["ui"]['sys'] = bgui.bge_utils.System(logic.expandPath('//themes/default'))
		globalDict["ui"]['sys1'] = bgui.bge_utils.System(logic.expandPath('//themes/default'))
		globalDict["ui"]['sys'].load_layout(MainUI, None)
		globalDict["ui"]['sys1'].load_layout(OverlayUI, None)
		globalDict["ui"]["sys"].add_overlay(MainMenu, None)
		mouse.visible = True

	else:
		globalDict["ui"]['sys'].run()
		globalDict["ui"]['sys1'].run()
