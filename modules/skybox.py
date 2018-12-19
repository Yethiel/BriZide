from bge import logic

from modules import helpers

def set_cam():
	sce = helpers.get_scene("Scene")
	own = logic.getCurrentController().owner
	cam = sce.active_camera

	if cam:
		own.worldOrientation = cam.worldOrientation
		own.fov = cam.fov