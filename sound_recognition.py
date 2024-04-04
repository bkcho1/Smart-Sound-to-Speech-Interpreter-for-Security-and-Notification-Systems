# Import necessary libraries
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from config import SOUNDS

# Define variables for audio recording
duration = 5  # Duration of audio recording in seconds
sample_rate = 44100  # Sample rate for audio recording (samples per second)
channels = 2  # Number of audio channels (2 for stereo)

def create_spectrogram(file):
    sample_rate, samples = wavfile.read(SOUNDS + '/' + file)

    if len(samples.shape) > 1:
        samples = samples.mean(axis=1)

    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    #plt.pcolormesh(times, frequencies, spectrogram)
    #plt.imshow(spectrogram)
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    #plt.show()
    
    return spectrogram

# Function to perform sound recognition
def recognize_sound(audio_data):
    # Placeholder function for sound recognition
    print("Recognizing sound...")
    # Your sound recognition algorithm here
    print("Sound recognition complete.")

