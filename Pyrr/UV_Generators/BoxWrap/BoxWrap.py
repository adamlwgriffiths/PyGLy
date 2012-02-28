'''
Created on 31/05/2011

@author: adam
'''

import numpy

from Pyrr.Plane import Plane
import Pyrr.Matrix.Matrix as Matrix
import Pyrr.Vector.Vector as Vector
from Pyrr.UV_Generators.UV_Generator import UV_Generator


class BoxWrap( UV_Generator ):
    
    
    def __init__( self, position, forward, up, size = (1.0, 1.0, 1.0) ):
        """
        Creates a Box with the bottom left corner at position with the normal
        being the depth and up the height
        @param position: Must be a numpy array
        @param normal: Must be a numpy array. The normal will be normalised
        during construction.
        @param up: Must be a numpy array and must be co-planar. The up vector
        will be normalised during construction.
        @param size: The size of the box where X is right, Y is forward, Z is up 
        @raise ValueError: raised if the up vector is not co-planar
        """
        super( BoxWrap, self ).__init__()
        
        self.position = numpy.array( position, dtype = float )
        self.size = size
        
        self.forward = numpy.array( forward, dtype = float )
        self.up = numpy.array( up, dtype = float )
        
        Vector.normalise( self.forward )
        Vector.normalise( self.up )
        
        if numpy.dot( self.forward, self.up ) != 0.0:
            raise ValueError( "Vectors are not co-planar" )
    
    def generateCoordinates( self, vertices, normals ):
        # use the normals to determine which side of the cube to map to
        # then use the vertices to map against that plane
        
        # determine our right vector
        right = numpy.cross( self.forward, self.up )
        
        # scale our vectors
        right *= self.size[ 0 ]
        forward = self.forward * self.size[ 1 ]
        up = self.up * self.size[ 2 ]
        
        # determine which axis a normal points toward
        dotProducts = numpy.empty( (3, len(normals)), dtype = float )
        
        dotRight = dotProducts[0,...]
        dotForward = dotProducts[1,...]
        dotUp = dotProducts[2,...]
        
        numpy.dot( normals, right, out = dotRight )
        numpy.dot( normals, forward, out = dotForward )
        numpy.dot( normals, up, out = dotUp )
        
        # make sure out dot products never go negative
        # this removes a lot of extra checking
        numpy.absolute( dotRight, out = dotRight )
        numpy.absolute( dotForward, out = dotForward )
        numpy.absolute( dotUp, out = dotUp )
        
        # create 2 arrays
        # we will do our dot products in a batch
        # these are the values we will dot against the vertices to
        # get our tu / tv coordinates
        tuDot = numpy.empty( (len(vertices), 3), dtype = float )
        tvDot = numpy.empty( (len(vertices), 3), dtype = float )
        
        for index in xrange( len( normals ) ):
            if ( \
                dotRight[ index ] >= dotForward[ index ] and \
                dotRight[ index ] >= dotUp[ index ] \
                ):
                # select the right face
                # forward for tu
                # up for tv
                tuDot[ index ] = forward
                tvDot[ index ] = up
            elif dotForward[ index ] >= dotUp[ index ]:
                # select the forward face
                # right for tu
                # up for tv
                tuDot[ index ] = right
                tvDot[ index ] = up
            else:
                # select the up face
                # right for tu
                # forward to tv
                tuDot[ index ] = right
                tvDot[ index ] = forward
        
        # now we perform a dot of the tu / tv against our vertices
        # and store the result in a texture coord array
        
        # create an empty texture coord array
        # dot product expects contiguous memory
        # so we have 2xN shape instead of Nx2 shape
        # we reshape after the dot product
        textureCoords = numpy.empty( (2, len(vertices)), dtype = float )
        
        # extract our rows
        tu = textureCoords[0,...]
        tv = textureCoords[1,...]
        
        # we can't use dot as the second vector is ND
        # and numpy will assume we mean a matrix calculation
        # http://www.mail-archive.com/numpy-discussion@scipy.org/msg04829.html
        print "vertices %s" % str(vertices)
        print "tuDot %s" % str(tuDot)
        print "tvDot %s" % str(tvDot)
        numpy.sum( vertices * tuDot, axis = 1, out = tu )
        numpy.sum( vertices * tvDot, axis = 1, out = tv )
        print "tu %s" % str(tu)
        print "tv %s" % str(tv)
        
        # reshape back into our normal Nx2 shape
        textureCoords = numpy.transpose( textureCoords )
        
        return textureCoords
    

if __name__ == "__main__":
    # ignored anyway
    normals = numpy.array([
        [ 0.0, -1.0, 0.0 ], # back = front face
        [ 0.0, -1.0, 0.0 ],
        [ 0.0, -1.0, 0.0 ],
        [ 0.0, -1.0, 0.0 ],
        [ 1.0, 0.0, 0.0 ],
        [ 1.0, 0.0, 0.0 ]
        ])
    
    vertices = numpy.array([
        [ 0.0, 0.0, 0.0 ],
        [ 0.25, 0.0, 0.0 ],
        [ 0.5, 0.0, 0.0 ],
        [ 1.0, 0.0, 0.0 ],
        [ 1.0, 0.5, 0.25 ],
        [ 1.0, 1.0, 0.5 ],
        ])
    
    # planer from x = 0.0 - +1.0
    # and from z = 0.0 to 1.0 
    position = numpy.array([ 0.0, 0.0, 0.0 ])
    forward = numpy.array([ 0.0, 1.0, 0.0 ])
    up = numpy.array([ 0.0, 0.0, 1.0 ])
    
    textureGen = BoxWrap(
        position = position,
        forward = forward,
        up = up,
        size = (5.0, 5.0, 5.0)
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