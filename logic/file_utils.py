from scipy.io import wavfile
from config import SOUNDS

def read(file, location):
    _, samples = wavfile.read(location + '/' + file)
    
    return samples

