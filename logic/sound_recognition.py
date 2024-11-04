# Import necessary libraries
from logic.file_utils import read
from logic.fingerprint import fingerprint
from logic.sound_IO import record_audio
from sqlite.connect import match, get, get_fingerprint_count
from datetime import datetime
import os

def recognize(file_name, directory):
    data = read(file_name, directory)

    hashes = set()

    fingerprints = []
    for i in range(data.ndim):
        fingerprints += fingerprint(data[:,i])

    hashes |= set(fingerprints)

    matches, countDict = match(hashes)

    if len(matches) == 0:
        return -1, -1, "Analyzed sound is not similar enough to stored sounds"

    sound_id = max(zip(countDict.values(), countDict.keys()))[1]
    predicted_sound_file_name = get(sound_id)

    return 1, sound_id, predicted_sound_file_name

def record_then_recognize(directory):
    filename = f"mic_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    record_audio(filename, directory)
    result = recognize(filename, directory)
    os.remove(os.path.join(directory, filename))

    return result