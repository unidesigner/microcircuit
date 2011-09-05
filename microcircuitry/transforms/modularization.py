"""
The ``modularization`` module provides functionality to compartmentalize
circuitry based on various criteria

"""

import numpy as np

def subcircuit_fromindex( circuit, indices ):
    """ Extract subcircuit from vertices indices
    """
    G = circuit.asgraph( add_attributes = True )
    return G.subgraph( indices )

def subcircuit( circuit, property, value, type = 'vertices'):
    """ Return subcircuit to extract a particular skeleton or subcircuit

    Parameters
    ----------
    property : str
    value : number
    type : {'vertices', 'connectivity'}
    
    """

    if type == 'vertices':
        prop = circuit.vertices_properties
    elif type == 'connectivity':
        prop = circuit.connectivity_properties
    else:
        raise Exception("Invalid `type` parameter")
    
    if prop.has_key( property ):
        if type == 'vertices':
            idx = np.where( prop[property]["data"] == value)[0]
        else:
            # extract the connections and retrieve the node indices
            idx = np.where( prop[property]["data"] == value)[0]
            idx = circuit.connectivity[ idx ].ravel()

        G = circuit.asgraph( add_attributes = True )
        return G.subgraph( idx )
    else:
        raise Exception("Property {0} does not exist".format(property))
    