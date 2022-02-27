import scipy as sp
import numpy as np


def fft_spectrum(signal, sr): # apply fft to find frequencies and their magnitudes in the segment 
    n = len(signal)
    
    freq_array = np.arange(n) * (float(sr)/n)
    freq_array = freq_array[:n//2]
    
    signal = signal - np.average(signal)
    freq_magnitude = np.fft.fft(signal)
    freq_magnitude = freq_magnitude[:n//2]
    
    freq_magnitude = np.abs(freq_magnitude)
    freq_magnitude /= np.sum(freq_magnitude)
    
    return freq_array, freq_magnitude
