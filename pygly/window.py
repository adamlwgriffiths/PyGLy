'''
Created on 02/03/2012

@author: adam
'''

import numpy

from pyrr import rectangle


def create_rectangle( window ):
    return numpy.array(
        [
            [ 0, 0 ],
            [ window.width, window.height ]
            ],
        dtype = numpy.int
        )

def aspect_ratio( rect ):
    """
    Returns the aspect ratio of the viewport.

    Aspect ratio is the ratio of width to height
    a value of 2.0 means width is 2*height
    """
    width = float(rect[ 1,0 ])
    height = float(rect[ 1,1 ])
    return width / height

