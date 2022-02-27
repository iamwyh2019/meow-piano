import librosa
from scipy.io import wavfile
from note_freq import note_freq_dict
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt
from utils import fft_spectrum
import json

with open("./data/2.4pv.json") as f:
    midijson = json.load(f)

tones = []
velocity_time_lists = {}

for note in midijson:


    tone = int(note["midi_note"])
    velocity = int(note["velocity"])
    if tone in tones:
        velocity_time_lists[tone][int(onset_time * self.sr)] = velocity
    else:
        tones.append(tone)
        velocity_time_lists[tone] = np.zeros(self.last_time * self.sr,)
        velocity_time_lists[tone][int(onset_time * self.sr)] = velocity


