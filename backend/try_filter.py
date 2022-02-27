import librosa
from scipy.io import wavfile
from note_freq import note_freq_dict
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt
from utils import fft_spectrum

a = {1:1, 2:3}

b = np.array(list(a.keys))

print(b[1])
