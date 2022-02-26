import scipy.signal as ss
import numpy as np
import librosa

import matplotlib.pyplot as plt


y, sr = librosa.load("./sound/F6.wav")
last_time = 20
output = np.zeros([last_time * sr,])

output[sr * 1] = 1
output[sr * 4] = 5
output[sr * 10] = 3

heiheihei = ss.convolve(output, y)

plt.figure()
plt.plot(y)
plt.show()

plt.figure()
plt.plot(heiheihei)
plt.show()
