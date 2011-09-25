import numpy as np

from .. import Circuit

metadata = {'name' : 'testcircuit'}

vert = np.array([[0, 0, 0],    # skeleton node (root)
                 [5, 5, 0],    # skeleton node
                 [10, 3, 0],   # connector
                 [15, 5, 0],   # skeleton node
                 [18, 0, 0],   # skeleton node (root)
                 [20, 0, 0]],  # skeleton node
                 dtype=np.float32)

conn = np.array([[0, 1],   # axonal
                 [1, 2],   # presyn
                 [3, 2],   # postsyn
                 [3, 4],   # dendritic
                 [4, 5]],  # dendritic
                 dtype=np.uint32)

vertices_properties = {
    "id": {"data": np.array([10, 11, 200, 20, 21, 22], dtype=np.uint32),
           "metadata": {}},
    # TODO: per node id, or skeletonid (but not for connector)
    "label": {"data": np.array([3, 1, 2, 1, 3, 1], dtype=np.uint32),
              "metadata": {
                    "type": "categorial",
                    "semantics": {
                        # TODO: branch node, leaf node etc.
                        1: {"name": "skeleton node", "ref": "XXX"},
                        2: {"name": "connector node", "ref": "XXX"},
                        3: {"name": "skeleton root node", "ref": "XXX"}
                    }
              }
    }
}

connectivity_properties = {
    "id": {"data": np.array([100, 100, 500, 500, 500], dtype=np.uint32),
            "metadata": {}
    },
    "type": {"data": np.array([1, 2, 3, 4, 4], dtype=np.uint32),
             "metadata": {
                    "type": "categorial",
                    "value": {
                        # TODO: unknown, spine head, spine neck
                        1: {"name": "axon", "ref": "XXX"},
                        2: {"name": "presynaptic_to", "ref": "XXX"},
                        3: {"name": "postsynaptic_to", "ref": "XXX",
                            "invert": True},
                        4: {"name": "dendrite", "ref": "XXX"}
                    }
                }
    }
}

testcircuit = Circuit(
        vertices=vert, connectivity=conn,
        vertices_properties=vertices_properties,
        connectivity_properties=connectivity_properties,
        metadata=metadata
    )