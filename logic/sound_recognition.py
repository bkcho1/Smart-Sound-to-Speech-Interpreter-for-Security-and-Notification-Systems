# Import necessary libraries
import soundfile as sf
from logic.file_utils import read
from logic.fingerprint import fingerprint
from sqlite.connect import match, get

def recognize(file_name):
    data = read(file_name)

    hashes = set()

    for i in range(data.ndim):
        fingerprints = fingerprint(data[:,i])
        hashes |= set(fingerprints)

    #print(hashes)
    matches, countDict = match(hashes)

    predicted_sound_file_name = get(max(zip(countDict.values(), countDict.keys()))[1])

    return predicted_sound_file_name
