'''
Created on 29/05/2011

@author: adam
'''

import numpy

from pygly.maths.plane import Plane
from pygly.maths import matrix
from uv_generator import UV_Generator


class Planar( UV_Generator ):
    """
    TODO: Should this use the normals or vertices?!
    """
    
    
    def __init__( self, position, normal, up, size = (1.0, 1.0) ):
        super( Planar, self ).__init__()
        
        self.plane = Plane( position, normal, up )
        self.size = size
    
    def generate_coordinates( self, vertices, normals ):
        # ignore the normals
        
        # create an empty texture coord array
        # dot product expects contiguous memory
        # so we have 2xN shape instead of Nx2 shape
        # we reshape after the dot product
        texture_coords = numpy.empty( (2, len(vertices)), dtype = float )
        
        # extract our rows
        tu = texture_coords[0,...]
        tv = texture_coords[1,...]
        
        # take our vertices and flatten them against the plane
        plane_vertices = matrix.apply_direction_scale(
            vertices,
            self.plane.normal,
            0.0
            )
        
        right = numpy.cross( self.plane.normal, self.plane.up )
        
        # get the tu / tv values from our up and right vectors
        numpy.dot( plane_vertices, right, out = tu )
        numpy.dot( plane_vertices, self.plane.up, out = tv )
        
        # apply our scaling
        tu /= self.size[ 0 ]
        tv /= self.size[ 1 ]
        
        # reshape back into our normal Nx2 shape
        texture_coords = numpy.transpose( texture_coords )
        
        return texture_coords
    

if __name__ == "__main__":
    # ignored anyway
    normals = []
    
    vertices = numpy.array([
        [ -1.0, 1.0, 0.0 ],
        [ 0.0, 0.0, 1.0 ],
        [ 0.5, 0.0, 0.5 ],
        [ 1.0, 0.0, 1.0 ]
        ])
    
    # planer from x = 0.0 - +1.0
    # and from z = 0.0 to 1.0 
    position = numpy.array([ 0.0, 0.0, 0.0 ])
    normal = numpy.array([ 0.0, 1.0, 0.0 ])
    up = numpy.array([ 0.0, 0.0, 1.0 ])
    
    texture_gen = Planar(
        position = position,
        normal = normal,
        up = up,
        size = (1.0, 1.0)
        )
    
    
    #print vertices
    texture_coords = texture_gen.generate_coordinates( vertices, normals )
    print "texture_coords %s" % str(texture_coords)
    
    assert texture_coords[ 0 ][ 0 ] == -1.0
    assert texture_coords[ 0 ][ 1 ] == 0.0
    assert texture_coords[ 1 ][ 0 ] == 0.0
    assert texture_coords[ 1 ][ 1 ] == 1.0
    assert texture_coords[ 2 ][ 0 ] == 0.5
    assert texture_coords[ 2 ][ 1 ] == 0.5

