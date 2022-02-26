from pydub import AudioSegment
from pydub.utils import get_array_type
import numpy as np
from matplotlib import pyplot as plt
import scipy
from note_freq import note_freq_dict, note, freq
import array


# Pitch detectior for piano part
def fft_spectrum(segment,array_type): # apply fft to find frequencies and their magnitudes in the segment 
    raw_data = array.array(array_type, segment._data)
    n = len(raw_data)
    
    freq_array = np.arange(n) * (float(segment.frame_rate)/n)
    freq_array = freq_array[:n//2]
    
    raw_data = raw_data - np.average(raw_data)
    freq_magnitude = np.fft.fft(raw_data)
    freq_magnitude = freq_magnitude[:n//2]
    
    freq_magnitude = np.abs(freq_magnitude)
    freq_magnitude /= np.sum(freq_magnitude)
    
    return freq_array, freq_magnitude

def find_note(freq): # Find the note with closest frequency
    # Some speical cases for weird sounds
    if freq < note_freq_dict[0][0]:
        return note_freq_dict[0][1]
    
    if freq > note_freq_dict[-1][0]:
        return note_freq_dict[-1][1]
    
    mindiff_index = 0
    mindiff = np.abs(freq - note_freq_dict[0][0])
    for i in range(1, len(note_freq_dict)):
        thisdiff = np.abs(freq - note_freq_dict[i][0])
        if thisdiff < mindiff:
            mindiff = thisdiff
            mindiff_index = i
    return note_freq_dict[mindiff_index][1]

def audio_pitch(filename):
    audio = AudioSegment.from_file('input_data/' + filename + '.wav')
    audio = audio.high_pass_filter(130).low_pass_filter(4000) # only deal with sounds within C3 - B7
    bit_depth = audio.sample_width * 8
    array_type = get_array_type(bit_depth) 

    window_len = 10 # break the audio into 10ms segments
    volume = [seg.dBFS for seg in audio[::window_len]] # volume of each segment
    time = np.arange(len(volume)) * (window_len/1000) # time for each segment (seconds)

    VOLUME_THRESHOLD = -40 # voices quieter than this is considered background noise
    EDGE_THRESHOLD = 3.4 # minimum rise in volume for a note
    TIME_BEFORE = 100 # minimum time between two consecutive notes (ms)
    notes = [] # store the notes time
    notes_amp = [] # store the notes amplitude
    for i in range(1,len(volume)):
        if volume[i]>VOLUME_THRESHOLD and volume[i]-volume[i-1]>EDGE_THRESHOLD: # loud enough, and a sudden rise in volume
            ms = i * window_len # note time
            if len(notes)==0 or ms-notes[-1]>TIME_BEFORE: # not too close to the previous note
                notes.append(ms)
                notes_amp.append(volume[i])

    notes_name = []
    notes_freq = []
    for start in notes:
        st, en = start, start+150 # take a 150ms segment
        segment = audio[st:en] # extract the segment
        freq,mag = fft_spectrum(segment,array_type) # compute frequency and amplitude with fft
        note_freq = freq[np.argmax(mag)] # find the frequency with maximum magnitude
        note_name = find_note(note_freq) # find the note's name
        notes_name.append(note_name)
        notes_freq.append(note_freq)
        #print(start/1000, note_name)

    plt.figure(figsize=(30,10), facecolor='white')
    plt.tick_params(labelsize=20)
    plt.plot(time, volume) # plot volume vs. time
    plt.title(filename, fontsize = 25)
    for note, amp, name in zip(notes, notes_amp, notes_name):
        plt.axvline(x=note/1000, color='r', linewidth=0.8, linestyle="-") # add a vertical line to each note
        plt.text(note/1000-0.2, amp+3, name, fontsize=20) # label each note's name
    plt.savefig('output_images/'+filename+'.png')
    
    return notes_freq, notes_name
'''
 the function returns the number of semitones between two given keys
 return: positive int means key1 down to key2, otherwise key1 raise to key2
'''
def steps_diff(key1, key2):
    info1, info2 = freq(key1, index = True), freq(key2, index =True)
    return info1[1] - info2[1]

'''
the function iterate the notelist of the audio files, 
check if note_list2 is the correct transposition of note_list1
'''
def transpose_checker(note_list1, note_list2, trans_step):
    mlen = min(len(note_list1), len(note_list2))
    wrong_notes = []
    if len(note_list1) != len(note_list2):
        print("Warning: note_list1 and note_list2 are of unequal length")
        print("Either you have different number of notes in the two files")
        print("or some notes are not correctly identified")
        print()
    for i in range(mlen):
        note1, note2 = note_list1[i],  note_list2[i]
        #print("in transpo checker", note1, note2, i)
        if steps_diff(note1,note2) != trans_step:
            tmp = freq(note1,index = True)
            note1_index = tmp[1]
            correct_note = note_freq_dict[note1_index-trans_step][1]
            wrong_notes.append([note1, note2, correct_note, i])
    
    score = str(mlen - len(wrong_notes)) + '/' + str(mlen)
    return wrong_notes, score


