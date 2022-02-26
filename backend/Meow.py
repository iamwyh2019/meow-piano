import this
import librosa
import numpy as np
import scipy.signal as ss

class Meow(object):

    def __init__(self, sr = 22050) -> None:
        self.sr = sr
        # self.origin_tone = 
        pass

    def sortByTone(self, midi):
        pass

    def generateSonglist(self, infos) -> np.ndarray:

        """
        tone
        amplitude
        starttime
        endtime
        """
        tones = infos["tones"]
        amplitude_time_lists = infos["amplitude_time_lists"]

        output = np.zeros(self.sr * self.lasttime)

        for tone in tones:
            this_tone = librosa.effects.pitch_shift(self.origin_tone, self.sr, n_steps = 89-tone)
            this_amplitude_time_list = amplitude_time_lists[tone]
            this_tone_output = ss.convolve(this_tone, this_amplitude_time_list)
        output += this_tone_output

        return output

