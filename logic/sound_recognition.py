# Import necessary libraries
import soundfile as sf
from logic.file_utils import read
from logic.fingerprint import fingerprint
from sqlite.connect import match, get, get_fingerprint_count

def recognize(file_name, directory):
    data = read(file_name, directory)

    hashes = set()

    fingerprints = []
    for i in range(data.ndim):
        fingerprints += fingerprint(data[:,i])

    hashes |= set(fingerprints)

    matches, countDict = match(hashes)

    sound_id = max(zip(countDict.values(), countDict.keys()))[1]
    predicted_sound_file_name = get(sound_id)

    if float(len(matches)) / float(get_fingerprint_count(sound_id)) <= 0.9:
        return -1, -1, "Analyzed sound is not similar enough to stored sounds"

    return 1, sound_id, predicted_sound_file_name
