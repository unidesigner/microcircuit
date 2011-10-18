"""

Microcircuit: Neural circuit analysis for neuroscience

The module has several sub-modules:

- ``circuit``: contains the constructors for circuit objects

- ``analysis``: analyzer classes that are circuit aware

- ``algorithms``: functions not-aware of the circuit semantics

- ``transforms``: ...


"""
__docformat__ = 'restructuredtext'

from .version import  __version__
from .circuit import Circuit

import transforms
import simulator
import dataset
import constants
import viz