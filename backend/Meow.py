import librosa
import numpy as np
import scipy.signal as ss
import os
import random

class Meow(object):

    def __init__(self, sr = 44100, last_time = 10) -> None:
        self.sr = sr
        self.last_time = last_time
        soundlist = os.listdir("./sound")
        self.tonedic = {}
        for sound in soundlist:
            sound_tone = int(sound.split(".")[0].split("_")[0])
            if sound_tone in soundlist:
                self.tonedic[sound_tone].append(sound)
            else:
                self.tonedic[sound_tone] = [sound]
        
        self.tonelist = np.array(list(self.tonedic.keys()), dtype=int)



    def transcriptMidijson(self, midijson):
        """
        Change the json file into 2 arrays.
        input: midi list like [{'onset_time': 0.6115822, 'offset_time': 1.22, 'midi_note': 43, 'velocity': 42},...]

        output:
        1. tones: np.1darray, contains all the tones detected
        2. velocity_time_lists: dictionary of {tones: velocity_time_list} contains the start time and amptitude of each tone
        """
        self.last_time = max(int(midijson[-1]["offset_time"]) + 2, self.last_time)
        tones = []
        velocity_time_lists = {}
        for note in midijson:

            tone = int(note["midi_note"])
            onset_time = float(note["onset_time"])
            velocity = int(note["velocity"])
            if tone in tones:
                velocity_time_lists[tone][int(onset_time * self.sr)] = velocity
            else:
                tones.append(tone)
                velocity_time_lists[tone] = np.zeros(self.last_time * self.sr,)
                velocity_time_lists[tone][int(onset_time * self.sr)] = velocity
            

        # self.tones = tones
        # self.velocity_time_lists = velocity_time_lists

        return tones, velocity_time_lists
    
    def pickMainTheme(self, windowinterval = 0.1, keepratio = 0.5):
        stepsize = int(self.sr * windowinterval / 2)
        windowsize = stepsize * 2
        velocity_time_matrix = np.zeros([len[self.tones], self.last_time * self.sr])
        for i in range(len(self.tones)):
            velocity_time_matrix[i,:] = self.velocity_time_lists[self.tones[i]]
        
        for i in range(0, velocity_time_matrix.shape[1] - windowsize, stepsize):
            threshold = np.sum(velocity_time_matrix[i:i+windowsize, :])




    def generateSonglist(self, tones, amplitude_time_lists) -> np.ndarray:
        """
        tone
        amplitude
        starttime
        endtime
        """
        output = np.zeros(self.sr * self.last_time)

        for tone in tones:
            modified_tone = self.chooseMeow(tone-12)
            if modified_tone is None:
                continue
            this_amplitude_time_list = amplitude_time_lists[tone]
            this_tone_output = ss.convolve(modified_tone, this_amplitude_time_list)[:output.shape[0]]
            output += this_tone_output

        return output

    def chooseMeow(self, tone):
        distance = np.abs(self.tonelist - tone)
        optional = self.tonelist[distance <= 6]
        if optional.shape[0] == 0:
            chosen_tone = self.tonelist[np.argmin(distance)]
            # return None
        else:
            chosen_tone = np.random.choice(optional)
        
        tone_files = self.tonedic[chosen_tone]
        chosen_file = random.choice(tone_files)
        this_tone, sr = librosa.load("./sound/{}".format(chosen_file), sr = self.sr)
        modified_tone = librosa.effects.pitch_shift(this_tone, self.sr, n_steps = tone - chosen_tone)
        return modified_tone

    # def chooseMeow(self, tone):
    #     distance = np.abs(self.meowlist - tone)
    #     optional = self.meowlist[distance <= 5]
    #     if optional.shape[0] == 0:
    #         optional = [self.meowlist[np.argmin(distance)]]

    #     modified_tones = []
    #     max_length = -1

    #     for chosen_tone in optional:
        
    #         tone_files = os.listdir("./sound/{}".format(chosen_tone))
    #         for chosen_file in tone_files:
    #             this_tone, sr = librosa.load("./sound/{}/{}".format(chosen_tone, chosen_file))
    #             # resample in case the sample rate of the sound file does not match the output file
    #             if sr != self.sr:
    #                 resample_number = int(this_tone.shape[0] / sr * self.sr)
    #                 this_tone = ss.resample(this_tone, resample_number)
                
    #             modified_tone = librosa.effects.pitch_shift(this_tone, self.sr, n_steps = tone - chosen_tone)
    #             max_length = max(max_length, modified_tone.shape[0])
    #             modified_tones.append(modified_tone)
    #     if len(modified_tones) == 1:
    #         return modified_tones[0]
    #     else:
    #         for i in range(len(modified_tones)):
    #             modified_tones[i] = np.pad(modified_tones[i],(0,max_length - len(modified_tones[i])),'constant',constant_values=(0,0))
    #         return np.average(np.array(modified_tones), axis = 0)


