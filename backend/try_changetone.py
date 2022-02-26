import librosa
from scipy.io import wavfile

import matplotlib.pyplot as plt

y, sr = librosa.load("./sound/F6.wav")
# 读取音频

# plt.figure()
# plt.plot(y)
# plt.show()

y_third = librosa.effects.pitch_shift(y, sr, n_steps = 4)

# plt.figure()
# plt.plot(y_third)
# plt.show()


wavfile.write("./output/cat2_add3.mp3", sr, y_third)
# # 写入音频

