import bge
import mathutils
import math
logic = bge.logic

def ship():
	own = logic.getCurrentController().owner
	ship = logic.getCurrentScene().objects["Ship"]
	own.fov = 100 + ship.localLinearVelocity.length * 0.2
	own.timeOffset = 12 - ship.localLinearVelocity.length/60 * 3
