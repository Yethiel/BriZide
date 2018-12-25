from bge import logic, events

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


def keystat(key, status):
    if status == "JUST_ACTIVATED":
        status = logic.KX_INPUT_JUST_ACTIVATED
    elif status == "JUST_RELEASED":
        status = logic.KX_INPUT_JUST_RELEASED
    elif status == "ACTIVE":
        status = logic.KX_INPUT_ACTIVE
    else:
        print("invalid status provided:", status, key)
        return False

    if getattr(events, key) in logic.mouse.events:
        return logic.mouse.events[getattr(events, key)] == status
    else:
        return logic.keyboard.events[getattr(events, key)] == status
