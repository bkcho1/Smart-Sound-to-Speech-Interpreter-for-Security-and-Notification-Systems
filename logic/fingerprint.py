import numpy as np
import hashlib
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (binary_erosion, generate_binary_structure, iterate_structure)
from config import DEFAULT_FS, DEFAULT_WINDOW_SIZE, DEFAULT_OVERLAP_RATIO, CONNECTIVITY_MASK, PEAK_NEIGHBORHOOD_SIZE, DEFAULT_AMP_MIN, MIN_HASH_TIME_DELTA, MAX_HASH_TIME_DELTA, FINGERPRINT_REDUCTION, DEFAULT_FAN_VALUE, SHOW

def fingerprint(channel_samples):
    spec, freq, t = mlab.specgram(channel_samples,NFFT=DEFAULT_WINDOW_SIZE,Fs=DEFAULT_FS,window=mlab.window_hanning,noverlap=int(DEFAULT_WINDOW_SIZE * DEFAULT_OVERLAP_RATIO))
    
    spec = 10 * np.log10(spec, out=np.zeros_like(spec), where=(spec != 0))
    
    if(SHOW):
        plt.pcolormesh(t, freq, spec, shading='auto')
        plt.show()

    peaks = find_peaks(spec)

    return generate_hashes(peaks)


def find_peaks(spec):
    struct = generate_binary_structure(2, CONNECTIVITY_MASK)

    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    local_max = maximum_filter(spec, footprint=neighborhood) == spec

    background = (spec == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    detected_peaks = local_max != eroded_background

    amps = spec[detected_peaks]
    freqs, times = np.where(detected_peaks)

    amps = amps.flatten()

    filter_idxs = np.where(amps > DEFAULT_AMP_MIN)

    freqs_filter = freqs[filter_idxs]
    times_filter = times[filter_idxs]

    if(SHOW):
        fig, ax = plt.subplots()
        ax.imshow(spec)
        ax.scatter(times_filter, freqs_filter)
        ax.set_aspect("auto")

        plt.gca().invert_yaxis()
        plt.show()
    
    return list(zip(freqs_filter, times_filter))

def generate_hashes(peaks):
    peaks.sort(key=itemgetter(1))

    hashes = []
    for i in range(len(peaks)):
        for j in range(1, DEFAULT_FAN_VALUE):
            if (i + j) < len(peaks):

                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

                if MIN_HASH_TIME_DELTA <= t_delta <= MAX_HASH_TIME_DELTA:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))

                    hashes.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], t1))
    if(SHOW):
        print(len(hashes))
        print(tuple(hashes))
    return hashes
