
# skeleton identifiers grouping the connective into individual morphologies
SKELETON_ID = 'skeletonid'

# Location key
LOCATION = 'location'

# type of vertices or connectivity
TYPE = 'type'

# name of the data key
DATA = 'data'

# name of the metadata key
METADATA = 'metadata'

# connector node
CONNECTOR_NODE = 'connector node'

# presynaptic connectivity
PRESYNAPTIC = 'presynaptic_to'

# postsynaptic connectivity
POSTSYNAPTIC = 'postsynaptic_to'

# gap junction
GAP_JUNCTION = 'connects_to_gap'

# connectome level

CONNECTOME_CHEMICAL_SYNAPSE = 'chemical synapse'
CONNECTOME_ELECTRICAL_SYNAPSE = 'electrical synapse'

space_unit_conversion = {
    'nm': 1,  # nanometer
    'um': 10 ** 3,  # micrometer
    'mm': 10 ** 6,  # millimeter
    'cm': 10 ** 7,  # centimeter
    'm': 10 ** 9  # meter
}

# The basic resolution
base_unit = 'nm'
