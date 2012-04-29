'''
Created on 29/04/2012

@author: adam
'''

import math


def calculate_fov( view_size, distance ):
    """
    http://www.glprogramming.com/red/chapter03.html
    """
    rad_theta = 2.0 * math.atan2( view_size / 2.0, distance )
    return math.degrees( rad_theta )

