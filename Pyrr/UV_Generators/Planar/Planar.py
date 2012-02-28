'''
Created on 29/05/2011

@author: adam
'''

import numpy

from Pyrr.Plane import Plane
import Pyrr.Matrix.Matrix as Matrix
import Pyrr.Vector.Vector as Vector
from Pyrr.UV_Generators.UV_Generator import UV_Generator


class Planar( UV_Generator ):
    """
    TODO: Should this use the normals or vertices?!
    """
    
    
    def __init__( self, position, normal, up, size = (1.0, 1.0) ):
        super( Planar, self ).__init__()
        
        self.plane = Plane( position, normal, up )
        self.size = size
    
    def generateCoordinates( self, vertices, normals ):
        # ignore the normals
        
        # create an empty texture coord array
        # dot product expects contiguous memory
        # so we have 2xN shape instead of Nx2 shape
        # we reshape after the dot product
        textureCoords = numpy.empty( (2, len(vertices)), dtype = float )
        
        # extract our rows
        tu = textureCoords[0,...]
        tv = textureCoords[1,...]
        
        # take our vertices and flatten them against the plane
        planeVertices = Matrix.applyDirectionScale(
            vertices,
            self.plane.normal,
            0.0
            )
        
        right = numpy.cross( self.plane.normal, self.plane.up )
        
        # get the tu / tv values from our up and right vectors
        numpy.dot( planeVertices, right, out = tu )
        numpy.dot( planeVertices, self.plane.up, out = tv )
        
        # apply our scaling
        tu /= self.size[ 0 ]
        tv /= self.size[ 1 ]
        
        # reshape back into our normal Nx2 shape
        textureCoords = numpy.transpose( textureCoords )
        
        return textureCoords
    

if __name__ == "__main__":
    import Pyrr.Vector as Vector
    
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
    
    textureGen = Planar(
        position = position,
        normal = normal,
        up = up,
        size = (1.0, 1.0)
        )
    
    
    #print vertices
    textureCoords = textureGen.generateCoordinates( vertices, normals )
    print "textureCoords %s" % str(textureCoords)
    
    assert textureCoords[ 0 ][ 0 ] == -1.0
    assert textureCoords[ 0 ][ 1 ] == 0.0
    assert textureCoords[ 1 ][ 0 ] == 0.0
    assert textureCoords[ 1 ][ 1 ] == 1.0
    assert textureCoords[ 2 ][ 0 ] == 0.5
    assert textureCoords[ 2 ][ 1 ] == 0.5


