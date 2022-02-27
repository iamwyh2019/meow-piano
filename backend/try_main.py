import scipy.signal as ss
import numpy as np
import librosa
import json
from scipy.io import wavfile

import matplotlib.pyplot as plt
from Meow import Meow


with open("./data/smile.json") as f:
    midijson = json.load(f)


Meaw_piano = Meow(allow_changetone = True, allow_highest_tone = 90, threshold = 0.8, window_interval = 0.1)
Meaw_piano.transcriptMidijson(midijson)
songlist = Meaw_piano.generateSonglist()

wavfile.write("./output/smile2.mp3", Meaw_piano.sr, songlist)
