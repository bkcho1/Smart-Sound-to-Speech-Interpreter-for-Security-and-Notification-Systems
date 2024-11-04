import sounddevice as sd
import soundfile as sf
from config import TEST  # Import TEST path from config.py
import os
from datetime import datetime
import pyttsx3

duration = 10  # Duration of recording in seconds
sample_rate = 44100  # Standard sample rate for audio
channels = 2  # Stereo

def record_audio(file_path):
    print(f"Recording audio for {duration} seconds...")

    # Record audio using sounddevice
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='float64')
    sd.wait()  # Wait until the recording is complete
    print("Recording complete.")

    # Ensure the directory for saving exists
    save_directory = os.path.dirname(file_path)
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"Created directory at {save_directory}")

    # Save the audio file
    sf.write(file_path, audio_data, sample_rate)
    print(f"Audio saved to {file_path}")

def play_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Test recording directly from sound_IO.py
    filename = f"test_mic_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    file_path = os.path.join(TEST, filename)
    record_audio(file_path)
