import sounddevice as sd
import soundfile as sf
import os
from datetime import datetime

duration = 5  # Duration of recording in secs
sample_rate = 44100  # Standard sample rate for audio (44.1 kHz)
channels = 2  # Stereo

# The path to save the recorded audio(in "sounds" folder)
sounds_folder = os.path.join(os.path.dirname(__file__), '../sounds')

# Ensure sounds directory exists
if not os.path.exists(sounds_folder):
    os.makedirs(sounds_folder)

def record_audio(filename):
    print(f"Recording audio for {duration} seconds...")

    # Record audio using "sounddevice"
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='float64')
    
    sd.wait()  # Wait until recording is done
    print("Recording complete.")

    # Full path to save the "".wav"
    file_path = os.path.join(sounds_folder, filename)
    
    # Save recorded audio as ".wav"
    sf.write(file_path, audio_data, sample_rate)
    print(f"Audio saved to {file_path}")

if __name__ == "__main__":
    # Create filename with a timestamp to avoid any overwriting files :)
    filename = f"mic_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    record_audio(filename)