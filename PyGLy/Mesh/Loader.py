# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 21:03:03 2011

@author: adam
"""

import os

# we need to inject our search paths before we
# load the pyassimp library
from pyassimp import helper

if os.name=='nt':
    helper.additional_dirs.append( r'C:\Users\adam\workspace\c++\assimp--2.0.863-sdk\bin\assimp_release-dll_win32' )

from pyassimp import pyassimp

# http://assimp.svn.sourceforge.net/viewvc/assimp/trunk/port/PyAssimp/sample.py?revision=406&content-type=text%2Fplain

pyassimp = pyassimp
