# Import necessary libraries
import soundfile as sf
from logic.file_utils import read
from logic.fingerprint import fingerprint
from sqlite.connect import match, get

def recognize(file_name, directory):
    data = read(file_name, directory)

    hashes = set()

    for i in range(data.ndim):
        fingerprints = fingerprint(data[:,i])
        hashes |= set(fingerprints)

    #print(hashes)
    matches, countDict = match(hashes)

    predicted_sound_file_name = get(max(zip(countDict.values(), countDict.keys()))[1])

    return predicted_sound_file_name


# # Import necessary libraries
# import soundfile as sf
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
# from scipy.io import wavfile
# from scipy.signal import argrelextrema
# from config import SOUNDS

# # Define variables for audio recording
# duration =   5 # Duration of audio recording in seconds
# sample_rate = 44100  # Sample rate for audio recording (samples per second)
# channels = 2  # Number of audio channels (2 for stereo)

# def create_spectrogram(file):
#     sample_rate, samples = wavfile.read(SOUNDS + '/' + file)

#     if len(samples.shape) > 1:
#         samples = samples.mean(axis=1)

#     frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

#     plt.pcolormesh(times, frequencies, spectrogram)
#     plt.imshow(spectrogram)
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Time [sec]')
#     plt.show()
    
#     return frequencies, times, spectrogram

# def find_local_maxima(file_name):
#     frequencies, times, spectrogram = create_spectrogram(file_name)

#     # Find local maxima
#     maxima_indices = argrelextrema(spectrogram, np.greater, axis=0)
#     maxima_freqs = frequencies[maxima_indices[0]]
#     maxima_times = times[maxima_indices[1]]

#     if len(maxima_freqs) > 0:
#         min_freq, max_freq = min(maxima_freqs), max(maxima_freqs)
#         print(f"Local maxima frequency range: {min_freq:.2f} Hz to {max_freq:.2f} Hz")
#     else:
#         print("No local maxima found.")

#     # Plot the spectrogram
#     plt.figure(figsize=(10, 6))
#     plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='auto')
#     plt.colorbar(label='Intensity [dB]')
#     plt.xlabel('Time [s]')
#     plt.ylabel('Frequency [Hz]')
#     plt.title('Spectrogram with Local Maxima')

#     # Plot the local maxima
#     plt.scatter(maxima_times, maxima_freqs, color='red', s=10, label='Local Maxima')
#     plt.legend()

#     plt.show()






    
# # Function to perform sound recognition
# def recognize_sound(audio_data):
#     # Placeholder function for sound recognition
#     print("Recognizing sound...")
#     # Your sound recognition algorithm here
#     print("Sound recognition complete.")

