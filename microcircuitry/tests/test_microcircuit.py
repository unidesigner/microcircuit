import numpy as np
import microcircuitry as mc

vert = np.array( [ [0,0,0], # skeleton node
                   [5,5,0], # skeleton node
                   [10,3,0], # connector
                   [15,5,0], # skeleton node
                   [18,0,0]], # skeleton node
                   dtype = np.float32 )

conn = np.array( [ [0, 1], # axonal
                   [1, 2], # presyn
                   [3, 2], # postsyn
                   [3, 4] ], # dendritic
                   dtype = np.uint32 )

vertices_properties = {
    "id" : { "data" : np.array( [10, 11, 200, 20, 21], dtype = np.uint32 ),
             "metadata" : {} },
    "label" : { "data" : np.array( [1, 1, 2, 1, 1], dtype = np.uint32 ),
                "metadata" : {
                    "type" : "categorial",
                    "semantics" : {
                        1 : { "name" : "skeleton node", "OBO" : "XXX" },
                        2 : { "name" : "connector node", "OBO" : "XXX" }
                    }
                }
    }
}

connectivity_properties = {
    "id" : { "data" : np.array( [100, 100, 500, 500], dtype = np.uint32 ),
             "metadata" : { }
    },
    "label" : { "data" : np.array( [1, 2, 3, 4], dtype = np.uint32 ),
                "metadata" : {
                    "type" : "categorial",
                    "semantics" : {
                        1 : { "name" : "axon", "OBO" : "XXX" },
                        2 : { "name" : "presynaptic_to", "OBO" : "XXX" },
                        3 : { "name" : "postsynaptic_to", "OBO" : "XXX", "invert" : True },
                        4 : { "name" : "dendrite", "OBO" : "XXX" }
                    }
                }
    }
}

circuit = mc.Microcircuit(
    vertices = vert,
    connectivity = conn,
    vertices_properties = vertices_properties,
    connectivity_properties = connectivity_properties
)

print circuit.to_graph( add_attributes=True ).edges( data = True )

subgraph = circuit.get_skeleton( 500 )
print subgraph.nodes( data = True )
print subgraph.edges( data = True )