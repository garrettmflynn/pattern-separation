
import numpy as np

def metadata(N,C):

    md = {
        'name': 'synthetic',
        'project': 'default-install',
        'fs': 2000,
        'all_streams': np.arange(C),
        'feature': 'spikes',
    }

    LEVELS = 3

    stream_pattern = np.zeros(max(md['all_streams'])+1, [('hierarchy', '<U256', LEVELS),\
                            ('positions', np.float32, LEVELS)])

    # ____________________________ Default Hippocampal Coordinates ____________________________

    rCA1 = np.array([25,-37,-0]) # CA1*RIGHT
    lCA1 = np.array([-25,-37,-0]) # CA1*LEFT
    rCA3 = np.array([28,-10,-22]) # CA3*RIGHT
    lCA3 = np.array([-28,-10,-22]) # CA3*LEFT
    INTERNAL_AP_AXIS = [0,2,0]
    rpCA1 = rCA1 - INTERNAL_AP_AXIS
    raCA1 = rCA1 + INTERNAL_AP_AXIS
    lpCA1 = lCA1 - INTERNAL_AP_AXIS
    laCA1 = lCA1 + INTERNAL_AP_AXIS
    rpCA3 = rCA3 - INTERNAL_AP_AXIS
    raCA3 = rCA3 + INTERNAL_AP_AXIS
    lpCA3 = lCA3 - INTERNAL_AP_AXIS
    laCA3 = lCA3 + INTERNAL_AP_AXIS

    # ___________________________________________ CA3 ___________________________________________

    stream_pattern['hierarchy'][md['all_streams'][np.arange(0,C/8).astype(int)]] = ['Right','CA3','Anterior']
    stream_pattern['positions'][md['all_streams'][np.arange(0,C/8).astype(int)]] = raCA3

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((C/8)),2*C/8).astype(int)]]  = ['Right','CA3','Posterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((C/8)),2*C/8).astype(int)]]  = rpCA3

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((2*C/8)),3*C/8).astype(int)]] = ['Left','CA3','Anterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((2*C/8)),3*C/8).astype(int)]] = laCA3

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((3*C/8)),4*C/8).astype(int)]] = ['Left','CA3','Posterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((3*C/8)),4*C/8).astype(int)]] = lpCA3


    # ___________________________________________ CA1 ___________________________________________

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((4*C/8)),5*C/8).astype(int)]] = ['Right','CA1','Anterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((4*C/8)),5*C/8).astype(int)]] = raCA1

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((5*C/8)),6*C/8).astype(int)]] = ['Right','CA1','Posterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((5*C/8)),6*C/8).astype(int)]] = rpCA1

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((6*C/8)),7*C/8).astype(int)]] = ['Left','CA1','Anterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((6*C/8)),7*C/8).astype(int)]] = laCA1

    stream_pattern['hierarchy'][md['all_streams'][np.arange(((7*C/8)),8*C/8).astype(int)]] = ['Left','CA1','Posterior']
    stream_pattern['positions'][md['all_streams'][np.arange(((7*C/8)),8*C/8).astype(int)]] = lpCA1

    stream_pattern = stream_pattern[md['all_streams']]

    md['stream_pattern'] = stream_pattern


    return md