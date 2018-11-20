from bge import logic

from modules import helpers

def set_cam():
	sce = helpers.get_scene("Scene")
	own = logic.getCurrentController().owner

	own.worldOrientation = sce.active_camera.worldOrientation
	own.fov = sce.active_camera.fov