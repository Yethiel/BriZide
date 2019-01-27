import bge
import mathutils
import math
from modules.helpers import clamp
logic = bge.logic

def ship():
	own = logic.getCurrentController().owner
	ship = logic.getCurrentScene().objects["Ship"]
	own.fov = clamp(100 + ship.localLinearVelocity.length * 0.2, 0.0, 200.0)
	own.timeOffset = clamp(12 - ship.localLinearVelocity.length/60 * 3, 0.2, 15.0)