from bge import logic

def clamp(value, min, max):
    """ Clamps the given value
    :param: value
    :param: min
    :param: max
    """
    if value > max:
        return max
    elif value < min:
        return min
    else:
        return value

def time_string(t):
    """ Interprets a float as seconds and returns a formatted string """
    return "{0:02d}:{1:02d}:{2}".format(int(t/60), int(t) % 60, str(t - int(t))[2:][:3])


def fatal_error(msg):
    print("Something went wrong:", msg)


def get_scene(scene_name):
    for sce in logic.getSceneList():
        if sce.name == scene_name:
            return sce
    return None