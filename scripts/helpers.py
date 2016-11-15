from bge import logic
"""
some shortcuts to make code more legible
"""

# just get stuff from the globalDict
def get_prop(key):
	return logic.globalDict.get(key)

def set_prop(key, value):
	logic.globalDict[key][value]

def clamp(value, min, max):
	if value > max:
		return max
	elif value < min:
		return min
	else:
		return value
