'''
Created on 29/05/2011

@author: adam
'''

import math

import numpy

from uv_generator import UV_Generator


class Spherical( UV_Generator ):
    
    
    def __init__( self, scale = (1.0, 1.0), offset = (0.0, 0.0) ):
        super( Spherical, self ).__init__()
        
        self.scale = scale
        self.offset = offset
    
    def generate_coordinates( self, vertices, normals ):
        # ignore the vertices
        
        # create an empty texture coord array
        texture_coords = numpy.empty( (len(normals), 2), dtype = float )
        
        # extract our columns
        normals_x = normals[:,0]
        normals_y = normals[:,1]
        normals_z = normals[:,2]
        
        tu = texture_coords[:,0]
        tv = texture_coords[:,1]
        
        # calculate tu
        numpy.arcsin( normals_z, tu )
        
        # calculate tu
        numpy.arctan2( normals_y, normals_x, tv )
        
        # arc sin gives a value between -1/2pi and +1/2pi
        tu /= numpy.pi
        tu += 0.5 + self.offset[ 0 ]
        
        # arc tangent give sa value between -pi and +pi
        tv /= (2.0 * numpy.pi)
        tv += 0.5 + self.offset[ 1 ]
        
        return texture_coords

