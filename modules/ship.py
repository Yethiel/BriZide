from bge import logic, events
globalDict = logic.globalDict
from modules import global_constants as G
import configparser, mathutils, os

co = logic.getCurrentController()
own = co.owner
sce = logic.getCurrentScene()
own["last_obj"] = None
own["thrust"] = 0.0

settings = globalDict["settings"]

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

# camera movement
key_thrust = getattr(events, c_stt["ship_thrust"])
key_thrust_reverse = getattr(events, c_stt["ship_thrust_reverse"])
key_steer_left = getattr(events, c_stt["ship_steer_left"])
key_steer_right = getattr(events, c_stt["ship_steer_right"])
key_activate_weapon = events.LEFTCTRLKEY
key_deactivate_stabilizer = getattr(events, c_stt["ship_deactivate_stabilizer"])
key_absorb_weapon = events.LEFTSHIFTKEY
key_pause = events.ESCKEY

def load(ship_name, player_id):
	settings = logic.globalDict.get("settings")
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
			"Grip" : 1.5,
			"GripAir" : 1,
			"SteerRate" : 0.5,
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
				ship_dict[category][key] = str(inf[category][key]).split("#")[0]
				if category == "Handling":  # Since the inf file will be loaded as strings, we need to cast them in this case.
					own[key] = float(ship_dict[category][key])
				else:  # Strings
					own[key] = ship_dict[category][key]
	if G.DEBUG:
		print("=== SHIP INFORMATION ===")
		for category in ship_dict:
			print(" > " + category + " < ")
			for key in ship_dict[category]:
				print("    " + str(key) + ": " + str(ship_dict[category][key]))

	logic.globalDict["current"]["ships"][player_id] = ship_dict
	own["player_id"] = player_id


# executed every tick to respond to key events
def controls():

	if globalDict.get("input")["focus"] == "ship":
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
		if  JUST_ACTIVATED in [keyboard.events[key_thrust], keyboard.events[key_thrust_reverse]]:
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

		if keyboard.events[key_deactivate_stabilizer] == JUST_ACTIVATED:
			own["restore"] = own.localLinearVelocity[1]
			own["stabilizer_boost"] = 0

		if keyboard.events[key_deactivate_stabilizer] == JUST_RELEASED:
			if own["stabilizer_boost"] > 1:
				own.localLinearVelocity[1] += own["restore"]
			else:
				pass # not enough power, discarding animation/sound

	# the stabilizer prevents the ship from drifting. the degree can vary from ship to ship
def stabilize():
	if keyboard.events[key_deactivate_stabilizer] == ACTIVE or not own["on_ground"]:
		if G.DEBUG: own['DEBUG_stabilizer'] = 'xxx'
	else:
		if own.localLinearVelocity[0] >= own["StableThreshold"]:
			own.applyForce([-own.localLinearVelocity[0]*own["StableStrength"],0,0], True)
			own.applyForce([0,abs(own.localLinearVelocity[0]),0], True)
			if G.DEBUG: own['DEBUG_stabilizer'] = '<--'
		elif own.localLinearVelocity[0] <= -own["StableThreshold"]:
			own.applyForce([-own.localLinearVelocity[0]*own["StableStrength"],0,0], True)
			own.applyForce([0,abs(own.localLinearVelocity[0]),0], True)

			if G.DEBUG: own['DEBUG_stabilizer'] = '-->'
		else:
			if G.DEBUG: own['DEBUG_stabilizer'] = '---'

# def thrust(d):
# 	t = own["timer_thrust"]
# 	if t < own["ThrustRate"]:f
# 		thrust = (t/own["ThrustRate"]) * own["ThrustRatio"]
# 	else:
# 		thrust = own["ThrustRatio"]
# 	if not own.localLinearVelocity[1] >= own["TopSpeed"]:
# 			own.applyForce([0,own["ThrustRatio"]*d,0], True)


def get_grip():
	if own["on_ground"]:
		return abs(1 - (own.localLinearVelocity[1]/own["TopSpeed"]) + own["Grip"])
	else:
		return own["GripAir"]


# when not steering, approximate 0 again (straight forward)
def center_steering():
	fps = logic.getLogicTicRate()
	if abs(own["turn"]) < abs(1/fps * own["SteerRate"]): own["turn"] = 0

	if own["turn"] > 0:
		own["turn"] -= (1/fps * own["SteerRate"])
	elif own["turn"] < 0:
		own["turn"] += (1/fps * own["SteerRate"])
	else:
		# own["turn"] = 0
		pass

	# own.applyRotation((0,0, own["turn"] ), True)

def steer(d):

	fps = logic.getLogicTicRate()

	if own.localLinearVelocity[1] < 0 and keyboard.events[key_thrust_reverse] == ACTIVE: d *= -1 # inverse steering when going reverse


	if own["turn"] > 0: #currently steering left
		if d < 0: # player wants left
			if abs(own["turn"]) <= own["SteerRatio"]: own["turn"] += (1/fps * own["SteerRate"]* get_grip())* -d

		elif d > 0: # player wants right
			# own["turn"] += (1/fps * own["SteerRate"])* -d   #center without respecting grip
			center_steering()


	elif own["turn"] < 0: #currently steering right
		if d < 0: # player wants left
			# own["turn"] += (1/fps * own["SteerRate"])* -d #center without respecting grip
			center_steering()
		elif d > 0: # player wants right
			if abs(own["turn"]) <= own["SteerRatio"]: own["turn"] += (1/fps * own["SteerRate"] * get_grip())* -d


	else:
		if abs(own["turn"]) <= own["SteerRatio"]: own["turn"] += (1/fps * own["SteerRate"]* get_grip())* -d

def center_thrust():
	fps = logic.getLogicTicRate()

	# if abs(own["thrust"]) < own["ThrustRate"] * 1/fps * 60:
	# 	own.localLinearVelocity.y = 0

	if own["thrust"] > 0:
		own["thrust"] -= own["ThrustRate"] * 1/fps * 60
	else:
		own["thrust"] += own["ThrustRate"] * 1/fps * 60

def thrust(d):

	fps = logic.getLogicTicRate()

	if abs(own["thrust"]) <= abs(own["ThrustRatio"]) and own.getLinearVelocity(True)[1] < own["TopSpeed"]:
		own["thrust"] += 1/fps * own["ThrustRate"] * d * 10


	# if own["thrust"] > 0: #currently steering left
	# 	if d < 0: # player wants left
	# 		if abs(own["thrust"]) <= own["ThrustRatio"]: own["thrust"] += (1/fps * own["ThrustRate"]* get_grip())* -d

	# 	elif d > 0: # player wants right
	# 		# own["thrust"] += (1/fps * own["ThrustRate"])* -d   #center without respecting grip
	# 		center_thrust()


	# elif own["thrust"] < 0: #currently Thrusting right
	# 	if d < 0: # player wants left
	# 		# own["thrust"] += (1/fps * own["ThrustRate"])* -d #center without respecting grip
	# 		center_thrust()
	# 	elif d > 0: # player wants right
	# 		if abs(own["thrust"]) <= own["ThrustRatio"]: own["thrust"] += (1/fps * own["ThrustRate"] * get_grip())* -d


	# else:
	# 	if abs(own["thrust"]) <= own["ThrustRatio"]: own["thrust"] += (1/fps * own["ThrustRate"]* get_grip())* -d


def activate_weapon():
	pass

def absorb_weapon():
	pass

def speedup():
	own.localLinearVelocity[1] = own["TopSpeed"]*1.5

def collision():
	own['energy'] -= abs(own.localLinearVelocity[1])/own["Shield"]/10

def descend():
	#TODO
	delta = 1/logic.getLogicTicRate()

	own.applyForce([0,0,-6000 * (delta)], True)

# main loop of the ship
def main():
	own["Velocity"] = own.localLinearVelocity[1]

	# own.applyRotation((0,0, own["turn"]), True)

	damping = own["HoverDamping"]
	height = own["HoverHeight"]
	strength = own["HoverStrength"]

	obj, point, normal = own.rayCast(own["dir_z_neg"], own, 10, "mag")
	stabilize()

	if obj != None:
		own["on_ground"] = True
		# print(normal[2])
		actual_dist = -own.getDistanceTo(point)
		distance = (actual_dist + height) # - own.localPosition.z
		cancel = -own.localLinearVelocity.z * damping * (distance + height)
		force = distance * strength + cancel
		own.applyForce([0, 0, force], True)
		own.alignAxisToVect(normal, 2, .2)

	else:
		descend()
		own["on_ground"] = False

	if globalDict.get("input")["focus"] == "ship":

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
	cube_size = globalDict["current"]["level"]["cube_size"]
	if own.worldPosition.z < -16:
		own.worldPosition.z += 5
	if own.worldPosition.z > cube_size * 32 - 16:
		own.worldPosition.z += 5

	if own.worldPosition.y > cube_size * 32 - 16:
		own.worldPosition.y -= 5
	if own.worldPosition.y < -16:
		own.worldPosition.y += 5

	if own.worldPosition.x > cube_size * 32 - 16:
		own.worldPosition.x -= 5
	if own.worldPosition.x < -16:
		own.worldPosition.x += 5

	# print(own.worldPosition)

def near():
	pass
	# i used to check for checkpoints here, but i'll put speed pads here later.
def setup():
	# load the ship information file (ShipDir is the directory to load the .inf from)
	load(globalDict.get("settings")["Game"]["ShipDir"], G.PLAYER_ID)

	# prepare the ship's own entry in the global dict
	globalDict["current"]["ships"][own["player_id"]]["last_checkpoint"] = None
	globalDict["current"]["ships"][own["player_id"]]["last_portal_id"] = None
	globalDict["current"]["ships"][own["player_id"]]["reference"] = own

	# set the start position according to the level
	own.worldPosition = globalDict.get("current")["level"]["start_pos"]

	# set the start orientation according to the level
	# for this we have to convert the euler matrix saved in the level file to a regular orientation matrix
	ship_orientation = own.worldOrientation.to_euler() # we need an euler matrix
	start_orientation = globalDict.get("current")["level"]["start_orientation"]
	for x in [0, 1, 2]:
		ship_orientation[x] = start_orientation[x]
	own.worldOrientation = ship_orientation.to_matrix()
	own["on_ground"] = False
