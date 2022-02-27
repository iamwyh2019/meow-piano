import librosa
import numpy as np
import scipy.signal as ss
import os
import random

class Meow(object):

    def __init__(self, sr = 44100, allow_changetone = True, allow_highest_tone = 95, threshold = 0.5, window_interval = 0.1) -> None:
        self.sr = sr

        # the Main Theme filter
        self.threshold = threshold
        self.window_interval = window_interval

        # the tone change
        self.allow_changetone = allow_changetone
        self.allow_highest_tone = allow_highest_tone

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
        self.last_time = int(midijson[-1]["onset_time"]) + 1

        midijson = self.adjustMidijson(midijson)

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

        self.tones = tones
        self.velocity_time_lists = velocity_time_lists

        return midijson

    def adjustMidijson(self, midijson):
        local_velocity = np.zeros(self.last_time * self.sr,)
        highest_tone = 0
        for note in midijson:
            tone = int(note["midi_note"])
            highest_tone = max(highest_tone, tone)
            onset_time = float(note["onset_time"])
            velocity = int(note["velocity"])
            local_velocity[int(onset_time * self.sr)] = max(velocity, local_velocity[int(onset_time * self.sr)])
        
        if (highest_tone > self.allow_highest_tone) and self.allow_changetone:
            lower_number = highest_tone - self.allow_highest_tone
        else:
            lower_number = 0
        
        new_midijson = []
        for note in midijson:
            onset_time = float(note["onset_time"])
            velocity = int(note["velocity"])
            if velocity > self.threshold * np.max(local_velocity[max(0, int((onset_time - self.window_interval/2) * self.sr)) : int(min(self.last_time, onset_time + self.window_interval/2) * self.sr)]):
                note["midi_note"] = str(int(note["midi_note"]) - lower_number)
                new_midijson.append(note)

        return new_midijson

        


    def generateSonglist(self) -> np.ndarray:
        """
        tone
        amplitude
        starttime
        endtime
        """
        output = np.zeros(self.sr * self.last_time, dtype=np.float64)

        for tone in self.tones:
            modified_tone = self.chooseMeow(tone)
            if modified_tone is None:
                continue
            this_amplitude_time_list = self.velocity_time_lists[tone]
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


