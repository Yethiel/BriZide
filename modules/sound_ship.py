import aud
from bge import logic
from modules import sound
from modules.helpers import clamp
sce = logic.getCurrentScene()

gD = logic.globalDict


def collision():
    pass
    # sound = aud.Factory.file(logic.expandPath("//wavs/collision1.wav"))
    # # sound = sound.pitch(2)
    # device.play(sound)


def mag():
    pass
    # cont = logic.getCurrentController()
    # own = cont.owner
    #
    # sound = cont.actuators['mag']
    #
    # Xspeed, Yspeed, Zspeed = own.getLinearVelocity(True)
    #
    # linvelocity = abs(Zspeed)
    #
    #
    # # velocity1 = linvelocity[1] * 0.4
    # # velocity0 = linvelocity[0] * 0.5 / 1.2
    # # velocity = 0
    # cont.activate(sound)
    #
    # sound.volume = abs(linvelocity)
    # sound.pitch = abs(linvelocity/ 22)

def engine():
    cont = logic.getCurrentController()
    own = cont.owner
    camera = sce.objects["Camera_Ship"]
    # camera = sce.active_camera
    if not "init_sound_engine" in own:
        # own["sound_engine"] = sound.play("engine")
        # own["sound_engine"].loop_count = -1
        # own["sound_engine"].relative = False
        # own["sound_engine"].distance_maximum = 64
        # own["sound_engine"].distance_reference = 0

        own["sound_engine"] = sound.EchoWrapper("engine", feedback=6, delay=0.07, loop=-1, relative=False, distance_maximum=64, distance_reference=8)
        own["sound_engine"].play()

        own["sound_air"] = sound.play("wind")
        own["sound_air"].loop_count = -1
        own["sound_air"].volume = 0
        own["sound_air"].relative = False
        own["sound_air"].distance_maximum = 32
        own["sound_air"].distance_reference = 0

        own["init_sound_engine"] = False
        # logic.device.doppler_factor = 1.2
        logic.device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR

    else:
        logic.device.listener_location = camera.worldPosition
        logic.device.listener_orientation = camera.worldOrientation.to_quaternion()
        # logic.device.listener_velocity = camera.getLinearVelocity()

        # own["sound_engine"].pitch = clamp(abs(own["thrust"]/own["ThrustRatio"]) + abs(own.getLinearVelocity(True)[1])/ 130, 0, 2.34)
        own["sound_engine"].set_pitch(clamp(abs(own["thrust"]/own["ThrustRatio"]) + abs(own.getLinearVelocity(True)[1])/ 130, 0.5, 2.3))
        own["sound_air"].volume = clamp((abs(own.getLinearVelocity(True)[0] + own.getLinearVelocity(True)[2]))/200, 0, 2)

        own["sound_engine"].set_location(own.worldPosition)
        own["sound_air"].location = own.worldPosition
