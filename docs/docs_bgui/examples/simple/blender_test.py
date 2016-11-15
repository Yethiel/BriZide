import sys

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bgui.bge_utils
import bge


class SimpleLayout(bgui.bge_utils.Layout):
	"""A layout showcasing various Bgui features"""

	def __init__(self, sys, data):
		super().__init__(sys, data)
		
		# Use a frame to store all of our widgets
		self.frame = bgui.Frame(self, border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

		# A themed frame
		self.win = bgui.Frame(self, size=[0.6, 0.8],
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			
		# Create an image to display
		self.win.img = bgui.Image(self.win, 'img.jpg', size=[.92, .7], pos=[.01, .24],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)
		
		# A button
		self.button = bgui.FrameButton(self.win, text='Click Me!', size=[.14, .09], pos=[.815, .03],
			options = bgui.BGUI_DEFAULT)
		self.audio_button = bgui.ImageButton(self.win, sub_theme='Audio',
										size=[0.05, 0.05], pos=[0.75, 0.05])
		# Setup an on_click callback for the image
		self.button.on_click = self.on_img_click

		# Add a label
		self.lbl = bgui.Label(self, text="I'm a label!", pos=[0, 0.9],
			sub_theme='Large', options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		
		# A couple of progress bars to demonstrate sub themes
		self.progress = bgui.ProgressBar(self.win, percent=0.0, size=[0.92, 0.06], pos=[.2, 0.17],
											sub_theme="Progress", options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
											
		self.health = bgui.ProgressBar(self.win, percent=0.5, size=[0.92, 0.02], pos=[0, 0.14],
											sub_theme="Health",	options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			
		# A few TextInput widgets
		self.input = bgui.TextInput(self.win, text="I'm active.", font="myfont.otf", size=[.4, .04], pos=[.04, 0.02],
			input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.input.activate()
		self.input.on_enter_key = self.on_input_enter
		
		self.input2 = bgui.TextInput(self.win, text="I select all when activated.", size=[.4, .04], pos=[.04, 0.08],
			input_options = bgui.BGUI_INPUT_SELECT_ALL, options = bgui.BGUI_DEFAULT)
		
		# A counter property used for the on_img_click() method
		self.counter = 0

	def on_input_enter(self, widget):
		self.lbl.text = "You've entered: " + widget.text
		widget.text = "You've locked this widget."
		widget.deactivate()
		widget.frozen = 1
		
	def on_img_click(self, widget):
		self.counter += 1
		self.lbl.text = "You've clicked me %d times" % self.counter
		self.progress.percent += .1
		if self.counter % 2 == 1:
			self.win.img.texco = [(1,0), (0,0), (0,1), (1,1)]
		else:
			self.win.img.texco = [(0,0), (1,0), (1,1), (0,1)]


def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = bgui.bge_utils.System('../../themes/default')
		own['sys'].load_layout(SimpleLayout, None)
		mouse.visible = True

	else:
		own['sys'].run()
