from bge import logic, events
sce = logic.getCurrentScene()

def keystat(key, status):

	if status == "JUST_ACTIVATED":
		status = logic.KX_INPUT_JUST_ACTIVATED
	if status == "JUST_RELEASED":
		status = logic.KX_INPUT_JUST_RELEASED
	if status == "ACTIVE":
		status = logic.KX_INPUT_ACTIVE

	if key in logic.mouse.events:
		return logic.mouse.key == status
	else:
		return logic.keyboard.key == status
