from __future__ import division
from __future__ import print_function
import vispy
import numpy as np
import math

def select(shader="separation",id=None, control_method='keyboard'):
    selection = {
        "separation": separation,
    }
    
    # Get the function from switcher dictionary
    func = selection.get(shader, lambda: "Invalid event parser")
    # Execute the function
    if (shader != 'separation'):
        return func()
    else:
        return func(id,control_method)


# ____________________________ CUSTOM ENVIRONMENTS ____________________________

def separation(id,control_method):

    from .gui import Engram
    from visbrain.objects import RoiObj
    from .objects import SourceObj, ConnectObj
    from visbrain.io import download_file

    # Create an empty kwargs dictionnary :
    kwargs = {}

    # ____________________________ DATA ____________________________

    # Load the xyz coordinates and corresponding subject name :
    # mat = np.load(download_file('xyz_sample.npz', astype='example_data'))
    # xyz, subjects = mat['xyz'], mat['subjects']

    metadata = id.durations[0].metadata
    binary = id.durations[0].bins[0]

    positions = metadata['stream_pattern']['positions']
    assignments = metadata['stream_pattern']['hierarchy']

    SPACING = 6 # In MNI coordinates
    INITIAL_DISTINCTIONS = []

    n_dims = np.shape(assignments)[1]
    existing_levels = []
    intersection_matrices = {}
    intersection_matrices['indices'] = np.empty([])
    intersection_matrices['streams'] = np.empty([])
    intersection_matrices['positions'] = np.empty([])
    intersection_matrices['hierarchy_lookup'] = []

    # Derive Intersection Matrix
    for k, hierarchy in enumerate(assignments):
        if '' not in hierarchy:
            intersection = []
            for level, v in enumerate(hierarchy):
                    if len(intersection_matrices['hierarchy_lookup']) <= level:
                        intersection_matrices['hierarchy_lookup'].append([])
                        intersection_matrices['hierarchy_lookup'][level].extend([v])
                    if v not in intersection_matrices['hierarchy_lookup'][level]:
                        intersection_matrices['hierarchy_lookup'][level].extend([v])
                    distinction = np.where(np.asarray(intersection_matrices['hierarchy_lookup'][level]) == v)[0][0]
                    intersection.append(distinction)
            if intersection:
                intersection = np.expand_dims(np.array(intersection), axis=0)
                pos = np.expand_dims(np.array(positions[k]), axis=0)
                stream = np.expand_dims(np.array(metadata['all_streams'][k]), axis=0)
                source_count = np.expand_dims(np.arange(np.array(sum(binary.nD_labels['1D']==metadata['all_streams'][k]))), axis=0)
                if k is 0:
                    intersection_matrices['indices'] = intersection
                    intersection_matrices['streams'] = stream
                    intersection_matrices['sources'] = source_count
                    intersection_matrices['positions'] = pos
                    
                else:
                    intersection_matrices['indices'] = np.append(intersection_matrices['indices'], intersection,axis=0)
                    intersection_matrices['streams'] = np.append(intersection_matrices['streams'], stream,axis=0)
                    intersection_matrices['sources'] = np.append(intersection_matrices['sources'],source_count+intersection_matrices['sources'][k-1][-1]+1,axis=0)
                    intersection_matrices['positions'] = np.append(intersection_matrices['positions'], pos,axis=0)

    xyz = position_slicer(intersection_matrices,method=INITIAL_DISTINCTIONS,ignore_streams=True)
    
    # Convert binary array into visualizable continuous values
    print('Calculating spike durations')
    TRAIL = 10
    TIMEPOINTS = 10000
    spikes = binary.data.T[0:TIMEPOINTS]
    one_array = np.where(spikes == 1)
    if not not one_array:
        lb_1 = one_array[0]-TRAIL
        ub_1 = one_array[0]
        lb_2 = one_array[0]
        ub_2 = one_array[0]+TRAIL
        for ii in range(len(lb_1)):
            if ub_2[ii] > len(spikes):
                ub_2[ii] = len(spikes)
            if lb_1[ii] < 0:
                lb_1[ii] = 0
                    
            spikes[lb_1[ii]:ub_1[ii],one_array[1][ii]] += np.linspace(0,1,ub_1[ii]-lb_1[ii])
            spikes[lb_2[ii]:ub_2[ii],one_array[1][ii]] += np.linspace(1,0,ub_2[ii]-lb_2[ii])
        
    spikes = spikes.T

    N = xyz.shape[0]  # Number of electrodes

    text = ['S' + str(k) for k in range(N)]
    s_obj = SourceObj('SourceObj1', xyz, data=spikes,color='crimson', text=text,alpha=.5,
                    edge_width=2., radius_min=1., radius_max=25.)

    
    connect = np.zeros((N, N,np.shape(spikes)[1]))
    valid = np.empty((N, N,np.shape(spikes)[1]))
    edges = np.arange(N)    

    print('Calculating connectivity')
    for ind,activity in enumerate(spikes):
        if ind < len(spikes):
            edge_activity = spikes[ind+1:-1]
            weight = edge_activity + activity
            valid = ((edge_activity > 0) & (activity > 0)).astype('int')
            connect[ind,ind+1:-1] = weight * valid

    umin = 0
    umax = np.max(spikes)

    c_obj = ConnectObj('ConnectObj1', xyz, connect,color_by='strength',
                    dynamic=(.1, 1.), cmap='gnuplot', vmin=umin + .1,
                    vmax=umax - 1,line_width=0.1,
                    clim=(umin, umax), antialias=True)


    r_obj = RoiObj('aal')
    # idx_rh = r_obj.where_is('Hippocampus (R)')
    # idx_lh = r_obj.where_is('Hippocampus (L)')
    # r_obj.select_roi(select=[idx_rh, idx_lh], unique_color=False, smooth=7, translucent=True)

    vb = Engram(source_obj=s_obj,roi_obj=r_obj,connect_obj=c_obj,metadata=metadata,\
                rotation=0.25,carousel_metadata=intersection_matrices,\
                    carousel_display_method='text',control_method=control_method)
    vb.engram_control(template='B1',alpha=.02)
    vb.engram_control(visible=False)
    vb.rotate(custom=(180-45.0, 0.0))
    vb.show()

def position_slicer(intersection_matrices, method=[],ignore_streams=True):

    SPACING = 1 # In MNI coordinates
    RESCALING = 100
    X = []
    Y = []
    Z = []
    # R = []
    # G = []
    # B = []
    # W = []

    indices = np.copy(intersection_matrices['indices'])
    positions = np.copy(intersection_matrices['positions'])
    sources = np.copy(intersection_matrices['sources'])

    dims = np.arange(np.shape(indices)[1])
    dissim = (dims != method)
    if method is []:
        dim_to_remove = dims
    else:
        dim_to_remove = np.where(dissim)[0]
    new_inds = indices
    new_inds[:,dim_to_remove] = 0
    groups, streams_in_groups,n_streams_in_group = np.unique(new_inds,axis=0,return_inverse=True,return_counts=True)
    group_pos = np.empty((np.shape(groups)[0],np.shape(positions)[1]))
    for ii,group in enumerate(groups):
        group_indices = np.where(streams_in_groups==ii)[0]
        group_pos[ii] = np.mean(positions[group_indices],axis=0)

    for group, group_properties in enumerate(groups):
        streams = np.squeeze(np.argwhere(np.all((new_inds-group_properties)==0, axis=1)))
        n_sources_in_group = sources[streams].size

        if ignore_streams:
            n_sources_in_streams = np.asarray([np.arange(n_sources_in_group)])
        else:
            n_sources_in_streams = sources[streams]

        for stream, source_inds in enumerate(n_sources_in_streams):
            source_inds -= source_inds[0]
            side = math.ceil((len(source_inds)-1)**(1./2.)) # (1./3.))
            side_1 = SPACING * ((source_inds//(side)) - ((side-1)/2))
            flatten = np.tile(0.,len(source_inds))
            side_2 = SPACING * ((source_inds%side) - ((side-1)/2)) #SPACING * ((((source/n_sources_in_group)%(side**2))//side) - (side-1)/2)
            
            if ignore_streams:
                X = np.append(X,group_pos[group][0] + side_1)
                Y = np.append(Y,group_pos[group][1] + flatten)
                Z = np.append(Z,group_pos[group][2] + side_2)
            else:
                X = np.append(X,group_pos[group][0] + flatten + (SPACING*stream))
                Y = np.append(Y,group_pos[group][1] + side_1)
                Z = np.append(Z,group_pos[group][2] + side_2)
                
            # R = np.append(R,np.tile(group/(len(groups)-1),len(source_inds)))
            # G = np.append(G,np.tile(group/(len(groups)-1),len(source_inds)))
            # B = np.append(B,np.tile(group/(len(groups)-1),len(source_inds)))
            # W = np.append(W,np.tile(1.,len(source_inds))) # Opacity 

    n_sources = sources.size

    if isinstance(dissim, (bool)):
        full = False
    elif (dims != method).any():
        full = False
    else:
        full = True



    # Recenter (to canvas) unless all distinctions have been made
    if not full:
        if len(np.unique(X)) > 1:
            X = ((X - np.min(X))/(max(X) - min(X))) - .5
        else:
            X = 0
        
        X = RESCALING * X

        if len(np.unique(Y)) > 1:
            Y = ((Y - min(Y))/(max(Y) - min(Y))) - .5
        else:
            Y = 0
        
        Y = RESCALING * Y

        if len(np.unique(Z)) > 1:
            Z = ((Z - min(Z))/(max(Z) - min(Z))) - .5
        else:
            Z = 0

        Z = RESCALING * Z

    xyz = np.zeros((n_sources,3)).astype('float32')
    # data = np.zeros(n_sources, [('a_color', np.float32, 4),
    #                     ('a_rotation', np.float32, 4)])

    xyz[:, 0] = X
    xyz[:, 1] = Y
    xyz[:, 2] = Z

    # data['a_color'][:, 0] = R
    # data['a_color'][:, 1] = G
    # data['a_color'][:, 2] = B
    # data['a_color'][:, 3] = W

    return xyz # , data