from bge import logic
from math import sin
import mathutils
from mathutils import Vector

def ship():
    """Animates the ship with some simple sines"""
    own = logic.getCurrentController().owner
    own.localPosition.z = own.localPosition.z + (sin(own["Time"]*1.5) * 0.007)
    own.localOrientation *= Vector([(sin(own["Time"]*1.7) * 0.02), -own.parent["turn"] * 4 + (sin(own["Time"]*1.5) * 0.02), 0])
