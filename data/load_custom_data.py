from engram.declarative import ID
from engram.procedural import events
from settings import customconfig
from scipy.io import loadmat
import neo
import numpy as np
import os

def neo_loader(md, dir='data'):
    # Load Signals Using Neo
    filename = os.path.join(dir, f"{md['name']}",
                                            f"{md['name']}{md['extensions']['signals']}")
    reader = neo.get_io(filename=filename)

    blks = reader.read(lazy=False)
    for blk in blks:
        for seg in blk.segments:
            raw_sigs = reader.get_analogsignal_chunk(block_index=0, seg_index=0)
            float_sigs = reader.rescale_signal_raw_to_float(raw_sigs, dtype='float64')
            data = np.transpose(float_sigs)
            fs = reader.get_signal_sampling_rate()
            units = reader.header['signal_channels'][0]['units']

    data = data[np.asarray(md['all_streams'])-1]

    # Load Events (including spikes)
    eventsname = os.path.join(dir, f"{md['name']}",
                                        f"{md['name']}{md['extensions']['events']}")
    reader = neo.get_io(filename=eventsname)
    events_, spikes_ = events.select(md['project'], reader)

    # Load Spikes (convert spikes to binary array + derive source channel)
    bin_chans = []
    spike_times = []
    for neuron in spikes_:
        spike_times.append(spikes_[neuron])
        bin_chans.append(int(neuron[3:6].lstrip('0')))

    id = ID(md)
    id.addDuration(conts=data, cont_channels=md['all_streams'], \
        bin_timestamps=spike_times, bin_channels=bin_chans)

    for ii, _ in enumerate(id.durations):
        for jj, _ in enumerate(id.durations[ii].bins):
            if id.durations[ii].conts[jj]:
                id.durations[ii].bins[jj].makeVectorsFromTimestamps(np.size(id.durations[ii].conts[jj].data,1))
            else:
                id.durations[ii].bins[jj].makeVectorsFromTimestamps()
    id.save()

    return id
