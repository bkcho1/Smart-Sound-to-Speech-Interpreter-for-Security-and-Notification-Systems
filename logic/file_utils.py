from scipy.io import wavfile

def read(file, location):
    _, samples = wavfile.read(location + '/' + file)
    
    return samples

