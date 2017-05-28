from bge import logic, events
gD = logic.globalDict
from modules import global_constants as G

import configparser, mathutils, os

co = logic.getCurrentController()
own = co.owner
sce = logic.getCurrentScene()
own["last_obj"] = None
own["thrust"] = 0.0

whl_fl = own.children["whl_fl"]
whl_fr = own.children["whl_fr"]
whl_bl = own.children["whl_bl"]
whl_br = own.children["whl_br"]

dir_neg_whl_fl = own.children["dir_neg_whl_fl"]
dir_neg_whl_fr = own.children["dir_neg_whl_fr"]
dir_neg_whl_bl = own.children["dir_neg_whl_bl"]
dir_neg_whl_br = own.children["dir_neg_whl_br"]


level = gD["current"]["level"]

settings = gD["settings"]

# get directions for raycasting
for obj in own.children:
	if "dir_z_pos" in obj.name:
		own["dir_z_pos"] = obj
	elif "dir_z_neg" in obj.name:
		own["dir_z_neg"] = obj

keyboard = logic.keyboard
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
JUST_RELEASED = logic.KX_INPUT_JUST_RELEASED
ACTIVE = logic.KX_INPUT_ACTIVE

#Key assignments Keyboard, will be loaded from settings

c_stt = settings["Controls_Player1"]

key_thrust = getattr(events, c_stt["ship_thrust"])
key_thrust_reverse = getattr(events, c_stt["ship_thrust_reverse"])
key_steer_left = getattr(events, c_stt["ship_steer_left"])
key_steer_right = getattr(events, c_stt["ship_steer_right"])
key_boost = getattr(events, c_stt["ship_boost"])
key_activate_weapon = events.LEFTCTRLKEY
key_deactivate_stabilizer = getattr(events, c_stt["ship_deactivate_stabilizer"])
key_absorb_weapon = events.LEFTSHIFTKEY
key_pause = events.ESCKEY

def load(ship_name, player_id):
	settings = gD.get("settings")

	ship_path = logic.expandPath("//ships/"+ship_name)
	inf_path = logic.expandPath("//ships/"+ship_name+"/"+ship_name+".inf")

	# load the information file
	inf = configparser.ConfigParser()
	if os.path.isfile(inf_path):
		inf.read(inf_path)
		if G.DEBUG: print("Loaded ship information file.")

	# Set default values. they will not be overwritten when they're missing from the ship's inf file.
	ship_dict = {
		"Main" : {
			"Name" : "Unknown",
			"Model" : "//ships/test/test.blend",
			"Texture" : "//ships/test/test.png",
			"Shadow" : "//ships/test/shadow.png",
		},
		"Handling" : {
			"TopSpeed" : 160,
			"ThrustRatio" : 50,
			"ThrustRate" : 6,
			"Grip" : 1,
			"GripAir" : 1,
			"SteerRate" : 0.3,
			"SteerRatio" : 0.04,
			"TurnAmount" : 0.04,
			"StableThreshold" : 0.01,
			"StableStrength" : 2,
			"Shield" : 100,
			"HoverHeight" : 6,
			"HoverStrength" : 200,
			"HoverDamping" : 2.5,
		}
	}

	# Replace parameters from inf file. Keys that aren't present won't be replaced.
	for category in ship_dict:
		
		for key in ship_dict[category]:
			
			if key in inf[category]:

				new_val = None # value to overwrite the default
				
				if category == "Handling":  # Since the inf file will be loaded as strings, we need to cast them in this case.
					set_success = True
					# new_val = float(inf[category][key]).split(";")[0].replace("\t", "")
					try:
						new_val = float(str(inf[category][key]).split(";")[0].replace("\t", ""))
					except Exception as e:
						if G.DEBUG: print(own.name + ":", "Could not set", key + ":", str(e))
						set_success = False
					
					if set_success: # Only overwrite default if the string could be parsed.
						ship_dict[category][key] = new_val
					
					own[key] = ship_dict[category][key]

				
				elif category == "Main": # These are supposed to be strings
					set_success = True
					try:
						new_val = str(inf[category][key]).split(";")[0].replace("\t", "")
					except:
						if G.DEBUG: print(own.name, ": Could not set", ship_dict[category][key])
						set_success = False
						
					if set_success: # Only set it if the string could be parsed.
						ship_dict[category][key] = new_val
					
					own[key] = ship_dict[category][key]
	if G.DEBUG:
		print("=== SHIP INFORMATION ===")
		for category in ship_dict:
			print(" > " + category + " < ")
			for key in ship_dict[category]:
				print("    " + str(key) + ": " + str(ship_dict[category][key]))

	gD["current"]["ships"][player_id] = ship_dict
	own["player_id"] = player_id


# executed every tick to respond to key events
def controls():

	if gD.get("input")["focus"] == "ship":
		if keyboard.events[key_thrust] == ACTIVE:
			thrust(1)
		if keyboard.events[key_thrust_reverse] == ACTIVE:
			thrust(-1)

		if not ACTIVE in [keyboard.events[key_thrust_reverse], keyboard.events[key_thrust]]:
			center_thrust()

		own.applyForce([0,own["thrust"],0], True)


		for thing in [JUST_ACTIVATED, JUST_RELEASED]:
			if thing in [keyboard.events[key_steer_left], keyboard.events[key_steer_right]]:
				pass
		if JUST_ACTIVATED in [keyboard.events[key_thrust], keyboard.events[key_thrust_reverse]]:
			pass

		if keyboard.events[key_activate_weapon] == JUST_ACTIVATED:
			#print("Activate weapon")
			own['lastkey'] = 'key_activate_weapon'
			activate_weapon()

		if keyboard.events[key_absorb_weapon] == JUST_ACTIVATED:
			#print("Absorb weapon")
			own['lastkey'] = 'key_absorb_weapon'
			absorb_weapon()

		if keyboard.events[key_pause] == JUST_ACTIVATED:
			print("Pause")
			own['lastkey'] = 'key_pause'

		# BOOST
		if keyboard.events[key_boost] == ACTIVE:
			if own["stabilizer_boost"] > 10:
				own.applyForce((0, own["ThrustRatio"]*2, 0), True)
				own["stabilizer_boost"] -= 2.5

# the stabilizer prevents the ship from drifting. the degree can vary from ship to ship
def stabilize():
	if keyboard.events[key_deactivate_stabilizer] == ACTIVE or not own["on_ground"]:
		if G.DEBUG: own['DEBUG_stabilizer'] = 'xxx'
	else:
		if abs(own.localLinearVelocity[0]) >= own["StableThreshold"]:
			own.applyForce([-own.localLinearVelocity[0]*own["StableStrength"] * get_grip(),0,0], True)
			own.applyForce([0,abs(own.localLinearVelocity[0]) * get_grip(),0], True)
		if G.DEBUG:
			if own.localLinearVelocity[0] >= own["StableThreshold"]:
				own['DEBUG_stabilizer'] = '<--'
			elif own.localLinearVelocity[0] <= -own["StableThreshold"]:
				own['DEBUG_stabilizer'] = '-->'
			else:
				own['DEBUG_stabilizer'] = '---'



def get_grip():
	if own["on_ground"] and not keyboard.events[key_deactivate_stabilizer] == ACTIVE:
		return abs(1 - (own.localLinearVelocity[1]/own["TopSpeed"]) + own["Grip"])
	else:
		return own["GripAir"]


# when not steering, approximate 0 again (straight forward)
def center_steering():
	delta = logic.getLogicTicRate()
	if abs(own["turn"]) < abs(1/delta * own["SteerRate"]): own["turn"] = 0

	if own["turn"] > 0:
		own["turn"] -= (1/delta * own["SteerRate"])
	elif own["turn"] < 0:
		own["turn"] += (1/delta * own["SteerRate"])
	else:
		# own["turn"] = 0
		pass

	# own.applyRotation((0,0, own["turn"] ), True)

def steer(d):

	delta = logic.getLogicTicRate()

	if own.localLinearVelocity[1] < 0 and keyboard.events[key_thrust_reverse] == ACTIVE: d *= -1 # inverse steering when going reverse

	# Smoothly center steering.
	if own["turn"] > 0: #currently steering left
		if d < 0: # player wants left
			if abs(own["turn"]) <= own["SteerRatio"]: own["turn"] += (1/delta * own["SteerRate"]* get_grip())* -d

		elif d > 0: # player wants right
			center_steering()

	# Smoothly center steering.
	elif own["turn"] < 0: #currently steering right
		if d < 0: # player wants left
			center_steering()
		elif d > 0: # player wants right
			if abs(own["turn"]) <= own["SteerRatio"]: own["turn"] += (1/delta * own["SteerRate"] * get_grip())* -d


	else:
		if abs(own["turn"]) <= own["SteerRatio"]: own["turn"] += (1/delta * own["SteerRate"]* get_grip())* -d

def center_thrust():
	delta = logic.getLogicTicRate()

	# if abs(own["thrust"]) < own["ThrustRate"] * 1/delta * 60:
	# 	own.localLinearVelocity.y = 0

	if own["thrust"] > 0:
		own["thrust"] -= own["ThrustRate"] * 1/delta * 60
	else:
		own["thrust"] += own["ThrustRate"] * 1/delta * 60

def thrust(d):
	delta = logic.getLogicTicRate()

	if abs(own["thrust"]) <= abs(own["ThrustRatio"]) and own.getLinearVelocity(True)[1] < own["TopSpeed"]:
		own["thrust"] += 1/delta * own["ThrustRate"] * d * 10

def activate_weapon():
	pass

def absorb_weapon():
	pass

def collision():
	own['energy'] -= abs(own.localLinearVelocity[1])/own["Shield"]/10

def descend():
	#TODO
	delta = 1/logic.getLogicTicRate()

	own.applyForce([0,0,-6000 * (delta)], True)

# main loop of the ship
def main():
	own["Velocity"] = own.localLinearVelocity[1]

	damping = own["HoverDamping"]
	height = own["HoverHeight"]
	strength = own["HoverStrength"]

	stabilize()

	# generate boost
	if abs(own.localLinearVelocity[0]) > 70:
		if own["stabilizer_boost"] < 500:
			own["stabilizer_boost"] += abs(own.localLinearVelocity[0])/120
		else:
			own["stabilizer_boost"] = 500 

	obj, point, normal = own.rayCast(own["dir_z_neg"], own, 2 * height, "mag")
	own["on_ground"] = True
	if obj != None:
		normalmed = mathutils.Vector((0,0,0))
		for whl in [(whl_fr, dir_neg_whl_fr), (whl_fl, dir_neg_whl_fl), (whl_bl, dir_neg_whl_bl), (whl_br, dir_neg_whl_br)]:
			obj, point, normal = own.rayCast(whl[1], whl[0], 2 * height, "mag")
			if obj != None:
				normalmed += normal
		if obj != None:
			actual_dist = -whl[0].getDistanceTo(point)
			distance = (actual_dist + height) # - whl[0].localPosition.z
			cancel = -whl[0].localLinearVelocity.z * damping * (distance + height)
			force = distance * strength + cancel
			own.applyForce([0, 0, force], True)
			own.alignAxisToVect(normalmed, 2, .2)

	else:
		descend()
		own["on_ground"] = False

	if gD.get("input")["focus"] == "ship":

		if keyboard.events[key_steer_left] == ACTIVE:
			own['lastkey'] = 'key_steer_left'
			steer(-1) # also accepts floats for analog controls

		if keyboard.events[key_steer_right] == ACTIVE:
			own['lastkey'] = 'key_steer_right'
			steer(1) # also accepts floats for analog controls

		if not ACTIVE in [keyboard.events[key_steer_right], keyboard.events[key_steer_left]]:
			center_steering()

		own.applyRotation((0,0, own["turn"] ), True) #actual steering happens here

	# catch ship out of cube
	level = gD["current"]["level"] # TODO(Yethiel): Remove when better loading is implemented
	cube_size = level.get_cube_size()
	if own.worldPosition.z < -16:
		own.worldPosition.z += 32
	if own.worldPosition.z > cube_size * 32 - 16:
		own.worldPosition.z += 32

	if own.worldPosition.y > cube_size * 32 - 16:
		own.worldPosition.y -= 32
	if own.worldPosition.y < -16:
		own.worldPosition.y += 32

	if own.worldPosition.x > cube_size * 32 - 16:
		own.worldPosition.x -= 32
	if own.worldPosition.x < -16:
		own.worldPosition.x += 32

	# print(own.worldPosition)

def near():
	pass
	# currently not used. near behavious should rather be used on blocks.

def setup():
	own["id"] = logic.game.register_ship(own)
	# load the ship information file (ShipDir is the directory to load the .inf from)
	load(gD.get("settings")["Game"]["ShipDir"], G.PLAYER_ID)

	# prepare the ship's own entry in the global dict
	gD["current"]["ships"][own["player_id"]]["last_checkpoint"] = None
	gD["current"]["ships"][own["player_id"]]["last_portal_id"] = None
	gD["current"]["ships"][own["player_id"]]["reference"] = own

	# set the start position according to the level
	own.worldPosition = level.get_start_pos()
	# set the start orientation according to the level
	# for this we have to convert the euler matrix saved in the level file to a regular orientation matrix
	ship_orientation = own.worldOrientation.to_euler() # we need an euler matrix
	start_orientation = level.get_start_orientation()
	for x in [0, 1, 2]:
		ship_orientation[x] = start_orientation[x]
	own.worldOrientation = ship_orientation.to_matrix()
	own["on_ground"] = False

	# Mark the ship component as loaded
	logic.components.mark_loaded("ship")





