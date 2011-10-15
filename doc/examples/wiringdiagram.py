from microcircuit.dataset.testcircuit002 import testcircuit as tc

from microcircuit.transforms.modularization import create_wiring_diagram

connectome = create_wiring_diagram(tc)