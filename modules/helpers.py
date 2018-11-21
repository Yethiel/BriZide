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

def time_string(timefloat):
    """ Interprets a float as seconds and returns a formatted string """
    return str( int(timefloat/60) ) + ":" + str(int(timefloat) % 60) + ":" + str(timefloat - int(timefloat))[2:][:3]

def fatal_error(msg):
    print("Something went wrong:", msg)


def get_scene(scene_name):
    for sce in logic.getSceneList():
        if sce.name == scene_name:
            return sce
    return None