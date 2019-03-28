from bge import logic, render
from modules import global_constants as G

def actuators():
    cont = logic.getCurrentController()
    act_bloom = cont.actuators["bloom"]
    act_blur = cont.actuators["blur"]

    if logic.settings["Video"]["blur"] == "True":
        if G.DEBUG: print("Blur activated")
        cont.activate(act_blur)

    if logic.settings["Video"]["bloom"] == "True":
        if G.DEBUG: print("Bloom activated")
        cont.activate(act_bloom)

def apply_settings():
    if float(logic.settings["Video"]["motion_blur"]) > 0.0:
        render.enableMotionBlur(float(logic.settings["Video"]["motion_blur"]))
    else:
        render.disableMotionBlur()
    if G.DEBUG: print("Motion blur: {}".format(float(logic.settings["Video"]["motion_blur"])))
    render.setFullScreen(logic.settings["Video"]["fullscreen"] == "True")
    render.setWindowSize(
            int(logic.settings["Video"]["width"]),
            int(logic.settings["Video"]["height"])
    )
    render.setGLSLMaterialSetting('lights', logic.settings["Video"]["lights"] == "True")
    render.setGLSLMaterialSetting('extra_textures', logic.settings["Video"]["extra_textures"] == "True")
