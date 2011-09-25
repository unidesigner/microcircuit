#! /usr/bin/env python
#
# Copyright (C) 2011 Stephan Gerhard <connectome@unidesign.ch>

descr   = """Python project for neural circuit analysis in neuroscience."""


import os
import sys

import microcircuit

DISTNAME         = 'microcircuit'
DESCRIPTION      = 'Python project for neural circuit analysis in neuroscience'
LONG_DESCRIPTION = descr
MAINTAINER       = 'Stephan Gerhard'
MAINTAINER_EMAIL = 'connectome@unidesign.ch'
URL              = 'http://unidesigner.github.com/microcircuit'
LICENSE          = 'BSD (3-clause)'
DOWNLOAD_URL     = 'http://github.com/unidesigner/microcircuit'
VERSION          = microcircuit.__version__

import setuptools # we are using a setuptools namespace
from numpy.distutils.core import setup


if __name__ == "__main__":
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(name = DISTNAME,
        maintainer  = MAINTAINER,
        include_package_data = True,
        maintainer_email = MAINTAINER_EMAIL,
        description = DESCRIPTION,
        license = LICENSE,
        url = URL,
        version = VERSION,
        download_url = DOWNLOAD_URL,
        long_description = LONG_DESCRIPTION,
        zip_safe=False, # the package can run out of an .egg file
        classifiers =
            ['Intended Audience :: Science/Research',
             'Intended Audience :: Developers',
             'License :: OSI Approved',
             'Programming Language :: Python',
             'Topic :: Software Development',
             'Topic :: Scientific/Engineering',
             'Operating System :: Microsoft :: Windows',
             'Operating System :: POSIX',
             'Operating System :: Unix',
             'Operating System :: MacOS'
             ],
         platforms='any',
         packages=['microcircuit', 'microcircuit.tests'],
         scripts=['bin/mne_clean_eog_ecg.py', 'bin/mne_flash_bem_model.py'])
