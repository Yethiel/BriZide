from bge import logic

def main():
	own = logic.getCurrentController().owner

	own.color[3] -= 0.001

	own.worldScale[0] += 0.01
	own.worldScale[1] += 0.01
	own.worldScale[2] += 0.01