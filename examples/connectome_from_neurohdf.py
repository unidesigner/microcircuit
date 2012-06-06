from microcircuit import *
import h5py
from microcircuit.connectome import Connectome

f=h5py.File('/home/stephan/dev/CATMAID/django/static/neurohdf/4h2qb1oi+55--9hv_t3sac(3ijdrtim2bq_t7hwnak32fvg90(.h5', 'r')
vertices_id = f['Microcircuit']['vertices']['id'].value
vertices_location = f['Microcircuit']['vertices']['location'].value
connectivity_id = f['Microcircuit']['connectivity']['id'].value
connectivity_skeletonid = f['Microcircuit']['connectivity']['skeletonid'].value
connectivity_type = f['Microcircuit']['connectivity']['type'].value

vertices_properties = {
    "location": {"data": vertices_location }
}

connectivity_properties = {
    "skeletonid": {"data": connectivity_skeletonid,
                   "metadata": {}
    },
    "type": {"data": connectivity_type,
             "metadata": {
                 "type": "categorial",
                 "value": {
                     0: {"name": "unknown"},
                     1: {"name": "axon", "ref": "XXX"},
                     2: {"name": "presynaptic", "ref": "XXX"},
                     3: {"name": "postsynaptic", "ref": "XXX"},
                     4: {"name": "dendrite", "ref": "XXX"}
                 }
             }
    }
}

a=Circuit(vertices_id, connectivity_id, connectivity_properties=connectivity_properties, vertices_properties=vertices_properties)
b=Connectome(circuit=a)