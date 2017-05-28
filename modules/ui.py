import sys
import bgui
import bgui.bge_utils
from bge import logic
from modules.ui_main_menu import MainMenu
from modules import global_constants as G


gD = logic.globalDict

class MainUI(bgui.bge_utils.Layout):
	def __init__(self, sys, data):
		super().__init__(sys, data)


# This is the topmost overlay for debug stuff
class OverlayUI(bgui.bge_utils.Layout):
	def __init__(self, sys, data):
		super().__init__(sys, data)
		self.frame = bgui.Frame(self, border=0)
		self.frame_load = bgui.Frame(self, border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]
		self.frame_load.colors = [(0, 0, 0, 0) for i in range(4)]

		self.lbl_fps = bgui.Label(self.frame, text="fps", pos=[0.1, 0.9], options = bgui.BGUI_DEFAULT)
		self.lbl_tck = bgui.Label(self.frame, text="tck", pos=[0.1, 0.85], options = bgui.BGUI_DEFAULT)
		self.lbl_rev = bgui.Label(self.frame, text="Brizide rev. " + G.REVISION, pos=[0.1, 0.1], options = bgui.BGUI_DEFAULT)
		self.lbl_velocity = bgui.Label(self.frame, text="velocity", pos=[0.9, 0.1], options = bgui.BGUI_DEFAULT)
		self.bar_boost = bgui.ProgressBar(self.frame, name="Boost", pos=[0.1, 0.1], options = bgui.BGUI_DEFAULT, percent = 0.0, size=[0.2,0.05])

		
		self.img_load = bgui.Image(self.frame_load, '//gfx/title.bmp', size=[1, 0.95], pos=[0, 0.05],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)
		
		self.bar_load = bgui.ProgressBar(self.frame_load, name="Boost", pos=[0, 0], options = bgui.BGUI_DEFAULT, percent = 0.0, size=[1,0.05])

		self.lbl_load = bgui.Label(self.frame_load, text="...", pos=[0.5, 0.015], options = bgui.BGUI_DEFAULT)


	def update(self):
		self.lbl_fps.text = str(int(logic.getAverageFrameRate()))
		self.lbl_tck.text = str(int(logic.getLogicTicRate()))
		if G.PLAYER_ID in gD["current"]["ships"]:
			self.bar_boost.percent = gD["current"]["ships"][G.PLAYER_ID]["reference"]["stabilizer_boost"]/500
			self.lbl_velocity.text = ">>> " + str(int(gD["current"]["ships"][G.PLAYER_ID]["reference"]["Velocity"]))

		if logic.components.is_loading():
			self.frame_load.visible = True
			self.bar_load.percent = logic.components.get_percent()
			self.lbl_load.text = logic.components.get_currently_loading()
		else:
			self.frame_load.visible = False


def main(cont):
	own = cont.owner
	mouse = logic.mouse

	if 'sys' not in logic.ui:
		logic.ui['sys'] = bgui.bge_utils.System(logic.expandPath('//themes/default'))
		logic.ui['sys1'] = bgui.bge_utils.System(logic.expandPath('//themes/default'))
		logic.ui['sys'].load_layout(MainUI, None)
		logic.ui['sys1'].load_layout(OverlayUI, None)
		logic.ui["sys"].add_overlay(MainMenu, None)
		mouse.visible = True

	else:
		logic.ui['sys'].run()
		logic.ui['sys1'].run()
