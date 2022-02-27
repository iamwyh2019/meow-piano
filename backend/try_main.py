import scipy.signal as ss
import numpy as np
import librosa
import json
from scipy.io import wavfile

import matplotlib.pyplot as plt
from Meow import Meow


Meaw_piano = Meow()
with open("./data/2.4pv.json") as f:
    midijson = json.load(f)


tones, velocity_amplitude_lists = Meaw_piano.transcriptMidijson(midijson)
songlist = Meaw_piano.generateSonglist(tones, velocity_amplitude_lists)

wavfile.write("./output/2.4pv.mp3", Meaw_piano.sr, songlist)
