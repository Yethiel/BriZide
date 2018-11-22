import aud
from bge import logic
from modules import global_constants as G
import os

logic.device = aud.device()

logic.sounds = {}
for wavpath in [logic.expandPath("//wavs/announcer/"), logic.expandPath("//wavs/")]:
    for wav in os.listdir(wavpath):
        if "engine" in wav:
            fac = aud.Factory.file(str(wavpath) + str(wav))
            logic.sounds[wav.replace('.ogg','')] = aud.Factory.buffer(fac)
        elif ".wav" in wav:
            logic.sounds[wav.replace('.wav','')] = aud.Factory.file(str(wavpath) + str(wav))
print(logic.sounds.keys())

class EchoWrapper():
    def __init__(self, soundstring, feedback=6, delay=0.07, dry=1, wet=0.3,
                loop=0, relative=False, distance_reference=0, distance_maximum=32):
        self.soundstring = soundstring
        self.feedback = feedback
        self.delay = delay
        self.wet = wet
        self.dry = dry
        self.loop = loop
        self.handles = []
        self.relative = relative
        self.distance_reference = distance_reference
        self.distance_maximum = distance_maximum

    def play(self):
        vol_sfx = float(logic.settings["Audio"]["effects"])

        for i in range(0, self.feedback):
            newfac = aud.Factory.delay(logic.sounds[self.soundstring], self.delay*i)
            snd = logic.device.play(newfac)

            snd.loop_count = self.loop
            snd.relative = self.relative
            snd.distance_reference = self.distance_reference
            snd.distance_maximum = self.distance_reference

            if i == 0:
                snd.volume = self.dry  * vol_sfx
            else:
                snd.volume = ( 1 - i/self.feedback ) * self.wet * vol_sfx
            self.handles.append(snd)

    def set_pitch(self, pitch):
        for snd in self.handles:
            snd.pitch = pitch
    def set_location(self, wposition):
        for snd in self.handles:
            snd.location = wposition

def play(facname):
    if facname in logic.sounds.keys():
        if G.DEBUG: print("Playing sound:",facname)
        snd = logic.device.play(logic.sounds[facname])
        snd.volume = float(logic.settings["Audio"]["effects"])
        return snd
    else:
        if G.DEBUG: print("Sound not found:", facname)
        return None

def init():
    logic.device.volume = float(logic.settings["Audio"]["master"])
