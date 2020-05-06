from engram.declarative import ID
from engram.procedural import events
from settings import customconfig
from scipy.io import loadmat
import neo
import numpy as np
import os

from data.generate_synthetic_data import spike_train
from data.generate_metadata import metadata
from data.load_custom_data import neo_loader

os.system('clear')

CUSTOM_DATA = False
LOAD_EXISTING_ID = False

if not CUSTOM_DATA:
    
    N = 100
    C = 25 # Must be divisible by 8 
    N_to_C = np.arange(N)%C

    md = metadata(N,C)

    id = ID(md)
    id.addDuration(bins=spike_train(N,5,fs=md['fs']), bin_channels=N_to_C)
    id.save()

else:

    md = {}
    md = customconfig.metadata

    if LOAD_EXISTING_ID:
        id = ID(md).load()
    
    else: 

        id = neo_loader(md, 'data')


id.episode(shader='separation', control_method='keyboard') # control_method='IR_Distance')