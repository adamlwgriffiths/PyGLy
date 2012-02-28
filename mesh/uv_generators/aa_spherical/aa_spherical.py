'''
Created on 29/05/2011

@author: adam
'''

import math

import numpy

from Pyrr.Plane import Plane
import Pyrr.Matrix.Matrix as Matrix
import Pyrr.Vector.Vector as Vector
from Pyrr.UV_Generators.UV_Generator import UV_Generator


class Spherical( UV_Generator ):
    
    
    def __init__( self, scale = (1.0, 1.0), offset = (0.0, 0.0) ):
        super( Spherical, self ).__init__()
        
        self.scale = scale
        self.offset = offset
    
    def generateCoordinates( self, vertices, normals ):
        # ignore the vertices
        
        # create an empty texture coord array
        textureCoords = numpy.empty( (len(normals), 2), dtype = float )
        
        # extract our columns
        normalsX = normals[:,0]
        normalsY = normals[:,1]
        normalsZ = normals[:,2]
        
        tu = textureCoords[:,0]
        tv = textureCoords[:,1]
        
        # calculate tu
        numpy.arcsin( normalsZ, tu )
        
        # calculate tu
        numpy.arctan2( normalsY, normalsX, tv )
        
        # arc sin gives a value between -1/2pi and +1/2pi
        tu /= numpy.pi
        tu += 0.5 + self.offset[ 0 ]
        
        # arc tangent give sa value between -pi and +pi
        tv /= (2.0 * numpy.pi)
        tv += 0.5 + self.offset[ 1 ]
        
        return textureCoords
    

if __name__ == "__main__":
    # ignored anyway
    vertices = []
    
    angleVector = numpy.array([ 1.0, 0.0, 1.0 ])
    angleVector = Vector.normalise( angleVector )
    
    normals = numpy.array([
        [ 1.0, 0.0, 0.0 ],
        [ 0.0, 0.0, 1.0 ],
        [ angleVector[ 0 ], angleVector[ 1 ], angleVector[ 2 ] ]
        ])
    
    textureGen = Spherical( scale = (2.0, 1.0), offset = (0.0, 0.0) )
    
    textureCoords = textureGen.generateCoordinates( vertices, normals )
    print "normals %s" % str(normals)
    print "textureCoords %s" % str(textureCoords)
    
    assert textureCoords[ 0 ][ 1 ] == 0.5


