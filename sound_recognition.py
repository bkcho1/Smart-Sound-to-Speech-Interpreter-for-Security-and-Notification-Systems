# Import necessary libraries
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy.signal import argrelextrema
from config import SOUNDS

# Define variables for audio recording
duration =   5 # Duration of audio recording in seconds
sample_rate = 44100  # Sample rate for audio recording (samples per second)
channels = 2  # Number of audio channels (2 for stereo)

def create_spectrogram(file):
    sample_rate, samples = wavfile.read(SOUNDS + '/' + file)

    if len(samples.shape) > 1:
        samples = samples.mean(axis=1)

    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    
    return frequencies, times, spectrogram

def find_local_maxima(file_name):
    frequencies, times, spectrogram = create_spectrogram(file_name)

    # Find local maxima
    maxima_indices = argrelextrema(spectrogram, np.greater, axis=0)
    maxima_freqs = frequencies[maxima_indices[0]]
    maxima_times = times[maxima_indices[1]]

    if len(maxima_freqs) > 0:
        min_freq, max_freq = min(maxima_freqs), max(maxima_freqs)
        print(f"Local maxima frequency range: {min_freq:.2f} Hz to {max_freq:.2f} Hz")
    else:
        print("No local maxima found.")

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='auto')
    plt.colorbar(label='Intensity [dB]')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.title('Spectrogram with Local Maxima')

    # Plot the local maxima
    plt.scatter(maxima_times, maxima_freqs, color='red', s=10, label='Local Maxima')
    plt.legend()

    plt.show()
    return maxima_freqs

# Function to analyze the relationship between two sound files

# def analyze_relationship(file1, file2):
#     maxima1 = find_local_maxima(file1)
#     maxima2 = find_local_maxima(file2)

#     if maxima1.size > 0 and maxima2.size > 0:
#         range1 = (min(maxima1), max(maxima1))
#         range2 = (min(maxima2), max(maxima2))

#         print(f"Local maxima frequency range for {file1}: {range1[0]:.2f} Hz to {range1[1]:.2f} Hz")
#         print(f"Local maxima frequency range for {file2}: {range2[0]:.2f} Hz to {range2[1]:.2f} Hz")

#         # If needed, add correlation or other analysis here
#     else:
#         print(f"No local maxima found in one or both of the files: {file1}, {file2}")


# Function to perform sound recognition
def recognize_sound(audio_data):
    # Placeholder function for sound recognition
    print("Recognizing sound...")
    # Your sound recognition algorithm here
    print("Sound recognition complete.")


