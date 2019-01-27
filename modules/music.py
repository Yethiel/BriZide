import aud
from os import listdir
from bge import logic
from random import shuffle, randint
from modules import global_constants as G

cont = logic.getCurrentController()
own = cont.owner

audio_settings = logic.settings["Audio"]

logic.music_device = aud.device()

music_list = []
global playing_index
playing_index = 0

own["init"] = False
own["handle"] = None
own["current_dir"] = logic.game.music_dir

def play(path):
    factory = aud.Factory.file(path)
    # play the audio, this return a handle to control play/pause
    return logic.music_device.play(factory)

def play_shuffle():
    global playing_index, music_list
    subdir = logic.game.music_dir
    if subdir:
        music_subdir = G.PATH_MUSIC + subdir
        change = own["current_dir"] != subdir

        if change or not own["init"]: # prepare the music list when it hasn't been initialized or when the music dir changed.
            music_list = []
            playing_index = 0
            own["current_dir"] = subdir # keep track of the directory this script is currently in

            for file in listdir(music_subdir):
                for type in G.TYPES_MUSIC:
                    if type in file:
                        music_list.append(file)
            shuffle(music_list)

            if G.DEBUG: print(own.name + "Available Music: " + str(music_list))

        if change:
            own["handle"].stop()

        IS_PLAYING = (hasattr(own["handle"], 'status') and own["handle"].status == True)

        if not own["init"] or not IS_PLAYING or change:
            own["handle"] = play(music_subdir + "/" + music_list[playing_index])

            if G.DEBUG: print(own.name + ": Now playing track " + str(playing_index) + ": " + music_list[playing_index])

            if playing_index + 1 > len(music_list)-1:
                playing_index = 0
            else:
                playing_index += 1

            # set the volume
            own["handle"].volume = float(audio_settings["Music"]) * float(audio_settings["Master"])
            own["init"] = True
