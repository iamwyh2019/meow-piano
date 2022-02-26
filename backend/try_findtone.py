import librosa
from scipy.io import wavfile
from note_freq import note_freq_dict

import scipy.signal as ss
import matplotlib.pyplot as plt
from utils import fft_spectrum

y, sr = librosa.load("./sound/cat1.wav")


freqs, magnitudes = fft_spectrum(y, sr)

peaks_idx, properties = ss.find_peaks(magnitudes, height=0.0001, distance=2000)

print(freqs[peaks_idx])
print(note_freq_dict)

plt.figure()
plt.plot(freqs, magnitudes)
plt.show()


