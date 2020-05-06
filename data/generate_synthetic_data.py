
from scipy.sparse import random

def spike_train(n,seconds,fs=2000):
    spikes = random(n,seconds*fs,density=0.005)
    spikes = (spikes.toarray() > 0).astype(int)
    

    return spikes

