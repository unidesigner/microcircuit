"""
Group microcircuitry elements (skeletons) based on different criteria:
- some size
- physiological properties
- dendritic morphology
- axon size
- conduction velocity
- incoming connectivity (classes of input cells)
- axon termination field
- ...

Requires a generic dataset with information per skeleton (e.g. neuron)

Pass a function which return boolean, combining the vertices and/or
connectivity properties as required to delineate the group

Highlight the selected group

"""

{

12 : { "type" : "Y-cell",
      "size" : "large",
      "summation" : "non-linear",
      "response" : "well to phasic or transient stimuli"}

}
