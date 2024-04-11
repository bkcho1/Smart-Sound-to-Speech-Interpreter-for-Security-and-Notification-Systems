from scipy.io import wavfile
from config import SOUNDS

def read(file):
    _, samples = wavfile.read(SOUNDS + '/' + file)
    
    return samples

