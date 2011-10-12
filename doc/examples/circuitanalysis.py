import numpy as np
import networkx as nx

import microcircuit as mc

tc = mc.dataset.testcircuit

def extract_value_customdict(dictionary, property, value='value', name='name'):
    for k,v in dictionary[value].items():
        if v[name] == property:
            return k
    return None

metc = tc.get_vertices_property('type', True)
mecotc = tc.get_connectivity_property('type', True)

connector_value = extract_value_customdict(metc, 'connector node')
presynaptic_value = extract_value_customdict(mecotc, 'presynaptic_to')
postsynaptic_value = extract_value_customdict(mecotc, 'postsynaptic_to')

vertices_type = tc.get_vertices_property('type')
connectivity_type = tc.get_connectivity_property('type')
connectivity_skeletonid = tc.get_connectivity_property('id')
connector_idx = set(np.where(vertices_type == connector_value)[0])

# loop over connectivity and extract connectors
# need to build potentially all polyadic (MxN) connectors
# key: vertices connector index, value: skeleton id
pre = dict.fromkeys(connector_idx, [])
post = dict.fromkeys(connector_idx, [])

for i,uv in enumerate(tc.connectivity):
    u,v = uv
    if v in connector_idx:
        # check if pre or post
        if connectivity_type[i] == presynaptic_value:
            pre[v].append(connectivity_skeletonid[i])
        elif connectivity_type[i] == postsynaptic_value:
            post[v].append(connectivity_skeletonid[i])
        else:
            print("Target node {0} neither pre nor postsynaptic".format(v))

G = nx.DiGraph()
G.add_nodes_from(np.unique(connectivity_skeletonid))
for cid in connector_idx:
    if not len(pre[cid]) == 0 and not len(post[cid]) == 0:
        # add M times N connectivity to network
        for u in pre[cid]:
            for v in post[cid]:
                # retrieve skeleton id for connectivity
                if G.has_edge(u,v):
                    G.edge[u][v]['weight'] += 1
                else:
                    G.add_edge(u,v, weight=1)
    else:
        print('Connector with either zero pre or post connectivity')

print(G.nodes(), G.edges(data=True))