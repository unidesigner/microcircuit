import numpy as np

if __name__ == '__main__':
    from microcircuit.dataset.testcircuit001 import testcircuit
    from copy import copy

    circ=copy(testcircuit)
    circg=circ.asgraph(True)
    
    # Extend vertices,edges representing segments with relevant parameters
    # for the time evolution
    for vertexid,d in circg.nodes_iter(data=True):
        # C_i is the capacitance of vertex i
        d['C_i']=2 # [pF]
        d['g_i_m']=2 # [pF]

    for u,v,d in circg.edges_iter(data=True):
        # g_ij is the conductance of segment between i and j
        # TODO: make it different depending on type!
        d['g_ij']=2 # [pS]

    # Global simulation parameters
    dt=0.1 # time step [s]
    total_time=1.0 # simulation duration
    n_ts=int(total_time/dt)
    
    # Establish a map between vertices id and array index
    n=len(circ.vertices)
    map_vertices_id2index = dict(zip(circ.vertices,range(n)))

    # Establish a map between connection ids and array index
    m=len(circ.connectivity)
    #map_connectivity_id2index = dict(zip(circ.vertices,range(len(vertices_id))))

    # Allocate memory to store the simulation results
    # dimension: number of vertices x number of time points
    membrane_potential = np.zeros((n,n_ts), dtype=np.float32)

    # Initialize membrane potential [mV]
    membrane_potential[:,0] = -60. + (np.random.rand(n)-0.5) * 10

    # APPLY EVOLUATION FUNCTION
    # Loop over time steps and compute new membrane potential
    for i in range(1,n_ts):
        print '======================'
        print 'new timestep', i
        # Loop over vertices to update with new value
        for vertexid,d in circg.nodes_iter(data=True):
            idx=map_vertices_id2index[vertexid]
            new_potential=0.0
            # all predecessors of current vertex
            # TODO: should mean all vertices that connect to vertexid
            pred=circg.predecessors(vertexid)
            for pid in pred:
                print 'predecessor', pid, 'for vertex', vertexid
                pidx=map_vertices_id2index[pid]
                # TODO: take length as a proxy for synaptic count
                weight=circg.edge[pid][vertexid]['length']/10.
                voltage_difference=(membrane_potential[pidx,i-1]-membrane_potential[idx,i-1])
                print 'weight', weight, 'voltage difference', voltage_difference
                # use conductance
                new_potential+=voltage_difference*circg.edge[pid][vertexid]['g_ij']

            new_potential-=d['g_i_m']*membrane_potential[idx,i-1]
            print 'oldpotential', membrane_potential[idx,i-1], 'newpotential', new_potential
            membrane_potential[idx,i]=new_potential
            print '-----'
            
    # Define a colormap for the potential to visualize microcircuit in fos (connection colors interpolated)
    