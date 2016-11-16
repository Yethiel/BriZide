"""
This is file for the level editor which can be used to create and manipulate tracks.
"""

import mathutils
from mathutils import Vector
from math import pi

from bge import logic, events, render
from modules import level, sound, global_constants as G

from modules.editor_ops import delete_block

gD = logic.globalDict

co = logic.getCurrentController()
own = co.owner
sce = logic.getCurrentScene()

sen_mouse = own.sensors["Over"]

# camera
obj_cam = sce.objects["Camera_Editor"]
cam_step = 5

winw = render.getWindowWidth()
winh = render.getWindowHeight()

pivot_cam = sce.objects["Pivot_Camera_Editor"]

settings = gD["settings"]
DEBUG = settings["Dev"]["debug"] == "True"
current_level = gD["current"]["level"]
selected_block = gD["editor"]["selected_block"]
own["mouse_cam_timeout"] = 0

# Step size of the editor. 16 seems to be alright (the editor will have an option to change this).
tile_size = 16

# The cursor object to place new blocks at.
obj_cursor = sce.objects["Cursor"]

keyboard = logic.keyboard
mouse = logic.mouse
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

#Key assignments Keyboard, will be loaded from settings
c_stt = settings["Controls_Editor"]

# camera movement
key_left = getattr(events, c_stt["editor_left"])
key_right = getattr(events, c_stt["editor_right"])
key_forward = getattr(events, c_stt["editor_forward"])
key_backward = getattr(events, c_stt["editor_backward"])
key_up = getattr(events, c_stt["editor_up"])
key_down = getattr(events, c_stt["editor_down"])
key_rotate_cam = getattr(events, c_stt["editor_rotate_cam"])

key_rotate_left = events.AKEY
key_rotate_right = events.DKEY
key_rotate_forward = events.WKEY
key_rotate_backward = events.SKEY
key_rotate_up = events.EKEY
key_rotate_down = events.QKEY
key_rotate = getattr(events, c_stt["editor_rotate"])

key_place = getattr(events, c_stt["editor_place"])
key_delete = getattr(events, c_stt["editor_delete"])
key_select = getattr(events, c_stt["editor_select"])
key_grab = getattr(events, c_stt["editor_grab"])

key_next = getattr(events, c_stt["editor_next"])
key_prev = getattr(events, c_stt["editor_prev"])

key_confirm = getattr(events, c_stt["editor_confirm"])
key_discard = getattr(events, c_stt["editor_discard"])

key_1 = getattr(events, c_stt["editor_1"])
key_2 = getattr(events, c_stt["editor_2"])
key_3 = getattr(events, c_stt["editor_3"])
key_4 = getattr(events, c_stt["editor_4"])
key_5 = getattr(events, c_stt["editor_5"])
key_6 = getattr(events, c_stt["editor_6"])
key_7 = getattr(events, c_stt["editor_7"])
key_8 = getattr(events, c_stt["editor_8"])
key_9 = getattr(events, c_stt["editor_9"])
key_10 = getattr(events, c_stt["editor_10"])

gD["input"]["focus"] = G.FOCUS_EDITOR_MAIN
gD["editor"]["rotation"] = {
	"axis": Vector([1, 1, 1]),
	"amount" : Vector([0, 0, 0]),
	"step_size" : pi/2,
	"original" : Vector([0, 0, 1])
}
gD["editor"]["grab"] = {
	"axis": [1, 1, 1],
	"amount" : Vector([0, 0, 0]),
	"step_size" : 16,
	"original" : [0,0,1],
}
gD["editor"]["active_block"] = obj_cursor
gD["editor"]["selected_block_index"] = 0

def controls():
	pass

### CURSOR

def move_cursor(vec):
	for c in range(0,3):
		vec[c] *= tile_size
	# apply movement in local mode
	obj_cursor.applyMovement(vec, True)

# aligning rather than rotating by pi/2 each time
# this is slightly more exact (at least i can sleep well now)
def rotate_cursor(vec):
	wo = obj_cursor.worldOrientation.to_euler()
	for x in [0, 1, 2]: wo[x] += vec[x]
	obj_cursor.worldOrientation = wo.to_matrix()
	# obj_cursor.alignAxisToVect(vec, axis, 1)
	# obj_cursor["rot_x"] += vec[0] % 2*pi
	# obj_cursor["rot_y"] += vec[1] % 2*pi
	# obj_cursor["rot_z"] += vec[2] % 2*pi
	# obj_cursor.applyRotation([obj_cursor["rot_x"], obj_cursor["rot_y"], obj_cursor["rot_z"]])

def refresh_cursor(selected_block):
	obj_cursor.replaceMesh(selected_block)
	# ui_title_obj["Text"] = selected_block
### PLACE AND DELETE BLOCKS

def place_block(selected_block):
	# place the selected block at the cursor's position
	sce.addObject(gD["editor"]["selected_block"], obj_cursor, 0)
	sound.play("checkpoint")

# delete block without selecting it first
def delete_block_imm():
	own["hitObject"].endObject()


# camera movement
def move_camera():
	if keyboard.events[key_left] == ACTIVE:
		# move_cursor([-1, 0, 0])
		pivot_cam.applyMovement([-cam_step, 0, 0], True)
	if keyboard.events[key_right] == ACTIVE:
		# move_cursor([1, 0, 0])
		pivot_cam.applyMovement([cam_step, 0, 0], True)

	if keyboard.events[key_forward] == ACTIVE:
		# move_cursor([0, 1, 0])
		pivot_cam.applyMovement([0, cam_step, 0], True)
	if keyboard.events[key_backward] == ACTIVE:
		# move_cursor([0, -1, 0])
		pivot_cam.applyMovement([0, -cam_step, 0], True)

	if key_up in keyboard.active_events or key_up in mouse.active_events:
	# if keyboard.active_events[key_up] == ACTIVE:
		pivot_cam.applyMovement([0, 0, cam_step], True)
		# move_cursor([0, 0, 1])
	if key_down in keyboard.active_events or key_down in mouse.active_events:
		pivot_cam.applyMovement([0, 0, - cam_step], True)
		# move_cursor([0, 0, -1])



	# prepare mouse camera control
	if mouse.events[key_rotate_cam] == JUST_ACTIVATED:
		own["old_mouse_pos"] = mouse.position # so we can reset the mouse position when we're done
		render.setMousePosition(int(winw / 2), int(winh / 2))
		mouse.visible = False

	#drag cam
	if mouse.events[key_rotate_cam] == ACTIVE and keyboard.events[events.LEFTSHIFTKEY] == ACTIVE and not mouse.visible:
		if own["mouse_cam_timeout"] > G.MOUSE_TIMEOUT:
			render.setMousePosition(int(winw / 2), int(winh / 2))
			mx = mouse.position[0] - 0.5
			my = mouse.position[1] - 0.5
			pivot_cam.applyMovement([0, 0, my * float(settings["Editor"]["cam_drag_amount"])], True)
			pivot_cam.applyMovement([-mx * float(settings["Editor"]["cam_drag_amount"]), 0, 0], True)
		else: own["mouse_cam_timeout"] += 1

	# drag cam forward
	elif mouse.events[key_rotate_cam] == ACTIVE and keyboard.events[events.LEFTCTRLKEY] == ACTIVE and not mouse.visible:
		if own["mouse_cam_timeout"] > G.MOUSE_TIMEOUT:
			render.setMousePosition(int(winw / 2), int(winh / 2))
			my = mouse.position[1] - 0.5
			pivot_cam.applyMovement([0, -my * float(settings["Editor"]["cam_drag_amount"]), 0], True)
		else: own["mouse_cam_timeout"] += 1

	# just rotate the camera
	elif mouse.events[key_rotate_cam] == ACTIVE and not mouse.visible:
		if own["mouse_cam_timeout"] > G.MOUSE_TIMEOUT:
			render.setMousePosition(int(winw / 2), int(winh / 2))
			mx = mouse.position[0] - 0.5
			my = mouse.position[1] - 0.5
			pivot_cam.applyRotation([0, 0.0, -mx], False)
			pivot_cam.applyRotation([-my, 0.0, 0], True)
		else: own["mouse_cam_timeout"] += 1


	# restore mouse position and show
	if mouse.events[key_rotate_cam] == JUST_RELEASED and not mouse.visible:
		mouse.visible = True
		mouse.position = own["old_mouse_pos"]
		own["mouse_cam_timeout"] = 0

### MODE OPERATIONS

# Enter rotation mode
def check_rotation_mode():
	if keyboard.events[key_rotate] == JUST_RELEASED:
		# original orientation of the block
		gD["editor"]["rotation"]["original"] = gD["editor"]["active_block"].worldOrientation.to_euler()
		mouse.visible = False

		gD["input"]["focus"] = G.FOCUS_EDITOR_ROT # set the input focus
		G.FOCUS_LOCK = True

		if G.DEBUG: print(own.name,"Rotation")

def check_grab_mode():
	# Enter grab mode
	if keyboard.events[key_grab] == JUST_RELEASED:
		# original orientation of the block
		orig_pos = gD["editor"]["active_block"].worldPosition
		for x in [0, 1, 2]: gD["editor"]["grab"]["original"][x] = gD["editor"]["active_block"].worldPosition[x]
		mouse.visible = False

		gD["input"]["focus"] = G.FOCUS_EDITOR_GRAB # set the input focus
		G.FOCUS_LOCK = True

		if G.DEBUG: print(own.name,"Grab")

def select_axis(mode):
	if keyboard.events[events.XKEY] == JUST_RELEASED:
		gD["editor"][mode]["axis"] = [1, 0, 0]
		if G.DEBUG: print(own, mode, "along x")
	if keyboard.events[events.YKEY] == JUST_RELEASED:
		gD["editor"][mode]["axis"] = [0, 1, 0]
		if G.DEBUG: print(own, mode, "along y")
	if keyboard.events[events.ZKEY] == JUST_RELEASED:
		gD["editor"][mode]["axis"] = [0, 0, 1]
		if G.DEBUG: print(own, mode, "along z")

def reset_mode(mode):
	gD["editor"][mode]["amount"] = Vector([0, 0, 0])


def rotation_mode():
	render.setMousePosition(int(winw / 2), int(winh / 2))
	mx = mouse.position[0] - 0.5
	my = mouse.position[1] - 0.5

	# select axis
	select_axis("rotation")

	vec = gD["editor"]["rotation"]["axis"]
	amnt = gD["editor"]["rotation"]["amount"]
	amnt += Vector([(mx-my)*vec[0], (mx-my)*vec[1], (mx-my)*vec[2]])
	# gD["editor"]["active_block"].applyRotation(Vector([(amnt[0] % pi) * pi, (amnt[1] % pi) * pi, (amnt[2] % pi) * pi]), False)
	ornt_new = gD["editor"]["active_block"].worldOrientation.to_euler()
	for x in [0, 1, 2]: ornt_new[x] = gD["editor"]["rotation"]["original"][x] + int(amnt[x]) * gD["editor"]["rotation"]["step_size"]
	gD["editor"]["active_block"].worldOrientation = ornt_new.to_matrix()

	# exit rotation mode and leave rotation applied
	if JUST_RELEASED in [keyboard.events[key_confirm], mouse.events[events.LEFTMOUSE]]:
		reset_mode("rotation")
		gD["input"]["focus"] = G.FOCUS_EDITOR_MAIN
		G.FOCUS_LOCK = False
		if G.DEBUG: print(own.name,"Leaving Rotation")
		mouse.visible = True

	# exit rotation mode and discard rotation
	if JUST_RELEASED in [keyboard.events[key_discard], mouse.events[events.RIGHTMOUSE]]:
		reset_mode("rotation")

		gD["editor"]["active_block"].worldOrientation = gD["editor"]["rotation"]["original"].to_matrix()
		gD["input"]["focus"] = G.FOCUS_EDITOR_MAIN
		G.FOCUS_LOCK = False
		if G.DEBUG: print(own.name,"Leaving Rotation, discarded changes")
		mouse.visible = True

def grab_mode():
	render.setMousePosition(int(winw / 2), int(winh / 2))
	mx = mouse.position[0] - 0.5
	my = mouse.position[1] - 0.5

	vec = gD["editor"]["grab"]["axis"]
	amnt = gD["editor"]["grab"]["amount"]
	amnt += Vector([(mx-my)*vec[0], (mx-my)*vec[1], (mx-my)*vec[2]])
	pos_new = gD["editor"]["active_block"].worldPosition
	for x in [0, 1, 2]: pos_new[x] = gD["editor"]["grab"]["original"][x] + int(amnt[x]) * gD["editor"]["grab"]["step_size"]
	gD["editor"]["active_block"].worldPosition = pos_new


	# select axis
	select_axis("grab")

	# for x in [0, 1, 2]:
	# 	gD["editor"]["active_block"].worldPosition[x] = obj_cursor.worldPosition[x] * gD["editor"]["grab"]["axis"][x]
	# if "CubeTile" in sen_mouse.hitObject.name:
	# 		obj_cursor.worldPosition = sen_mouse.hitObject.worldPosition
	# else:
	# 	obj_cursor.worldPosition = sen_mouse.hitObject.worldPosition
	# 	for x in [0, 1, 2]:
	# 		obj_cursor.worldPosition[x] += sen_mouse.hitNormal[x] * 32


	# exit grab mode and leave translation applied
	if JUST_RELEASED in [keyboard.events[key_confirm], mouse.events[events.LEFTMOUSE]]:
		reset_mode("grab")
		gD["input"]["focus"] = G.FOCUS_EDITOR_MAIN
		mouse.visible = True
		if G.DEBUG: print(own.name,"Leaving Grab")

	# exit grab mode and discard translation
	if JUST_RELEASED in [keyboard.events[key_discard], mouse.events[events.RIGHTMOUSE]]:
		reset_mode("grab")
		gD["editor"]["active_block"].worldPosition = gD["editor"]["grab"]["original"]
		gD["input"]["focus"] = G.FOCUS_EDITOR_MAIN
		mouse.visible = True
		if G.DEBUG: print(own.name,"Leaving Grab, discarded changes")


def main():

	if keyboard.events[events.LEFTCTRLKEY] == ACTIVE: # all controls that require CTRL to be held down
		if keyboard.events[events.SKEY] == JUST_RELEASED:
			level.save()

### ROTATION MODE
	if gD["input"]["focus"] == G.FOCUS_EDITOR_ROT:
		rotation_mode()

### GRAB MODE
	elif gD["input"]["focus"] == G.FOCUS_EDITOR_GRAB:
		grab_mode()

### SELECT BLOCK TO PLACE
	if keyboard.events[events.RIGHTARROWKEY] == JUST_RELEASED:
		gD["editor"]["selected_block_index"] += 1
		gD["editor"]["selected_block"] = gD["current"]["block_list"][gD["editor"]["selected_block_index"]]
		refresh_cursor(gD["editor"]["selected_block"])
	if keyboard.events[events.LEFTARROWKEY] == JUST_RELEASED:
		gD["editor"]["selected_block_index"] -= 1
		gD["editor"]["selected_block"] = gD["current"]["block_list"][gD["editor"]["selected_block_index"]]
		refresh_cursor(gD["editor"]["selected_block"])

	# what to do when we're not in one of the manipulation modes
	if gD["input"]["focus"] == G.FOCUS_EDITOR_MAIN:

		move_camera()

		# select object
		if sen_mouse.hitObject != None:
			own["hitObject"] = sen_mouse.hitObject

			if mouse.events[key_select] == JUST_ACTIVATED:
				gD["editor"]["active_block"] = own["hitObject"]
			# gD["editor"]["active_block"].visible = False

			if "CubeTile" in sen_mouse.hitObject.name:
				obj_cursor.worldPosition = sen_mouse.hitObject.worldPosition
			else:
				obj_cursor.worldPosition = sen_mouse.hitObject.worldPosition
				for x in [0, 1, 2]:
					obj_cursor.worldPosition[x] += sen_mouse.hitNormal[x] * 32

		# Place the selected block and restore the cursor after it
		if mouse.events[key_place] == JUST_ACTIVATED:
			place_block(selected_block)
			gD["editor"]["selected_block"] = None
			refresh_cursor("Cursor")

		# Delete the current active block
		if keyboard.events[key_delete] == JUST_ACTIVATED:
			delete_block()

		# Hover over block and delete it immediately for Kons
		if keyboard.events[events.LEFTSHIFTKEY] == ACTIVE and mouse.events[events.RIGHTMOUSE] == JUST_RELEASED:
			delete_block_imm()

		# Check and set UI focus for manipulation modes
		check_rotation_mode()
		check_grab_mode()








	# wor = pivot_cam.worldOrientation.to_euler()
	#
	# xp = pivot_cam.getAxisVect([1, 0, 0])[1]
	# xn = pivot_cam.getAxisVect([-1, 0, 0])[1]
	# yp = pivot_cam.getAxisVect([0, 1, 0])[1]
	# yn = pivot_cam.getAxisVect([0, -1, 0])[1]
	# zp = pivot_cam.getAxisVect([0, 0, 1])[1]
	# zn = pivot_cam.getAxisVect([0, 0, -1])[1]
	#
	# dirlist = [xp, xn, yp, yn, zp, zn]
	#
	# # print(dirlist)
	# print(pivot_cam.getAxisVect([0, 0, 1]))
	# print("xp", xp == max(dirlist))
	# print("xn", xn == max(dirlist))
	# print("yp", yp == max(dirlist))
	# print("yn", yn == max(dirlist))
	# print("zp", zp == max(dirlist))
	# print("zn", zn == max(dirlist))
	#
	# if yp == max(dirlist) or yn == max(dirlist) or xn == max(dirlist) or xp == max(dirlist):
	# pivot_cam.applyRotation([0, 0.0, -mx], True)
	# pivot_cam.applyRotation([-my, 0.0, 0], True)
	# if zp == max(dirlist) or zn == max(dirlist):
	# 	pivot_cam.applyRotation([0, -mx, 0], False)
	# 	pivot_cam.applyRotation([-my, 0.0, 0], True)
	# else:
	# 	pivot_cam.applyRotation([0, -mx, 0], False)
	# 	pivot_cam.applyRotation([-my, 0.0, 0], True)
	# if not mouse.events[key_rotate_cam] == ACTIVE:
	# 	pivot_cam.applyRotation([0, 0.0, -mx], True)
	# 	pivot_cam.applyRotation([-my, 0.0, 0], True)
	# else:
	# 	# pivot_cam.applyRotation([my, 0.0, 0], True)
	# 	pivot_cam.applyRotation([0, mx, 0], True)
	# 	# SET NEW Z AXIS
