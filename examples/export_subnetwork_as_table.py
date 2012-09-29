# Load NeuroHDF exported from CATMAID

import microcircuit as mc
import csv

#c=mc.load_neurohdf('/lhome/stephan/Downloads/abd15.h5', '/Microcircuit')
c=mc.load_neurohdf('/lhome/stephan/Downloads/stem1.h5', '/Microcircuit')

all_skeletons = c.get_all_skeletons()

sk = c.get_skeleton( all_skeletons[0] )
print sk.get_total_length()
print sk.get_neuron_name()
print sk.get_incoming_connector_nodes()

# class IV abd1.5
#classIV = [14463820, 14428936, 14426460, 14475920, 14478068, 14512656]
#targets = [15053048,15030726,14738006,14742032,14976562,14991314,16028668,16011828,15077568,14958382,14759770,14766914,14905150,14920814,15528762]

# class IV stem (segment 2)
classIV = [17612493,0,17399036,17467876,0,17590984]
targets = [17778726,17633542,17399984,17537182,17531577,17400196,0,17507543,17470353,0,17460403,17507639]

g=c.get_subgraph( filter(lambda a:a!=0, classIV + targets) )
g.edges(data=True)
g.nodes(data=True)

# FIXME: synaptic counts not correct
# does order of insert matter?

def export_subnetwork( filename, inputs, outputs, g ):
    """ Exports the connectivity between inputs and outputs
    as a table in csv format """

    with open(filename, 'wb') as csvfile:
        circuitwriter = csv.writer(csvfile, delimiter='|')
        
        firstrow = ['Skeleton ID','Neuron Name'] 
        for sens in inputs:
            if not g.has_node( sens ):
                firstrow.append( 'PLACEHOLDER' )
                firstrow.append( '' )
                continue
            firstrow.append( g.node[sens]['neuron_name'] )
            firstrow.append( '' )
        firstrow += ['total count', '']
        circuitwriter.writerow( firstrow )

        secondrow = ['','']
        secondrow += ['onto','from'] * (len(inputs)+1)
        circuitwriter.writerow( secondrow )

        for tar in outputs:
            
            if g.has_node( tar ):
                newrow = [tar, g.node[tar]['neuron_name'] ]
            else:    
                newrow = [0, 'PLACEHOLDER' ]
            
            for sens in inputs:
                # incoming count from sensory to target
                if g.has_edge(sens, tar):
                    newrow.append( g.edge[sens][tar]['synaptic_count'] )
                else:
                    newrow.append( 0 )
                    
                # outgoing count from target to sensory    
                if g.has_edge(tar,sens):
                    newrow.append( g.edge[tar][sens]['synaptic_count'] )
                else:
                    newrow.append( 0 )
                    
            # sum
            onto_cnt = sum(newrow[2::2])
            from_cnt = sum(newrow[3::2])
            newrow += [onto_cnt, from_cnt]
            
            circuitwriter.writerow( newrow )

export_subnetwork( '/lhome/stephan/stem1.csv', classIV, targets, g)
