'''
Created on 31/05/2011

@author: adam
'''

import numpy

import maths.vector
from uv_generator import UV_Generator


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
        
        maths.vector.normalise( self.forward )
        maths.vector.normalise( self.up )
        
        if numpy.dot( self.forward, self.up ) != 0.0:
            raise ValueError( "Vectors are not co-planar" )
    
    def generate_coordinates( self, vertices, normals ):
        # use the normals to determine which side of the cube to map to
        # then use the vertices to map against that plane
        
        # determine our right vector
        right = numpy.cross( self.forward, self.up )
        
        # scale our vectors
        right *= self.size[ maths.vector.x ]
        forward = self.forward * self.size[ maths.vector.y ]
        up = self.up * self.size[ maths.vector.z ]
        
        # determine which axis a normal points toward
        dot_products = numpy.empty( (3, len(normals)), dtype = float )
        
        dot_right = dot_products[ maths.vector.x, ... ]
        dot_forward = dot_products[ maths.vector.y, ... ]
        dot_up = dot_products[ maths.vector.z, ... ]
        
        numpy.dot( normals, right, out = dot_right )
        numpy.dot( normals, forward, out = dot_forward )
        numpy.dot( normals, up, out = dot_up )
        
        # make sure out dot products never go negative
        # this removes a lot of extra checking
        numpy.absolute( dot_right, out = dot_right )
        numpy.absolute( dot_forward, out = dot_forward )
        numpy.absolute( dot_up, out = dot_up )
        
        # create 2 arrays
        # we will do our dot products in a batch
        # these are the values we will dot against the vertices to
        # get our tu / tv coordinates
        tu_dot = numpy.empty( (len(vertices), 3), dtype = float )
        tv_dot = numpy.empty( (len(vertices), 3), dtype = float )
        
        for index in xrange( len( normals ) ):
            if ( \
                dot_right[ index ] >= dot_forward[ index ] and \
                dot_right[ index ] >= dot_up[ index ] \
                ):
                # select the right face
                # forward for tu
                # up for tv
                tu_dot[ index ] = forward
                tv_dot[ index ] = up
            elif dot_forward[ index ] >= dot_up[ index ]:
                # select the forward face
                # right for tu
                # up for tv
                tu_dot[ index ] = right
                tv_dot[ index ] = up
            else:
                # select the up face
                # right for tu
                # forward to tv
                tu_dot[ index ] = right
                tv_dot[ index ] = forward
        
        # now we perform a dot of the tu / tv against our vertices
        # and store the result in a texture coord array
        
        # create an empty texture coord array
        # dot product expects contiguous memory
        # so we have 2xN shape instead of Nx2 shape
        # we reshape after the dot product
        texture_coords = numpy.empty( (2, len(vertices)), dtype = float )
        
        # extract our rows
        tu = texture_coords[ 0, ... ]
        tv = texture_coords[ 1, ... ]
        
        # we can't use dot as the second vector is ND
        # and numpy will assume we mean a matrix calculation
        # http://www.mail-archive.com/numpy-discussion@scipy.org/msg04829.html
        print "vertices %s" % str(vertices)
        print "tu_dot %s" % str(tu_dot)
        print "tv_dot %s" % str(tv_dot)
        numpy.sum( vertices * tu_dot, axis = 1, out = tu )
        numpy.sum( vertices * tv_dot, axis = 1, out = tv )
        print "tu %s" % str(tu)
        print "tv %s" % str(tv)
        
        # reshape back into our normal Nx2 shape
        texture_coords = numpy.transpose( texture_coords )
        
        return texture_coords
    

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
    
    texture_gen = BoxWrap(
        position = position,
        forward = forward,
        up = up,
        size = (5.0, 5.0, 5.0)
        )
    
    
    #print vertices
    texture_coords = texture_gen.generate_coordinates( vertices, normals )
    print "textureCoords %s" % str(texture_coords)
    
    assert texture_coords[ 0 ][ 0 ] == -1.0
    assert texture_coords[ 0 ][ 1 ] == 0.0
    assert texture_coords[ 1 ][ 0 ] == 0.0
    assert texture_coords[ 1 ][ 1 ] == 1.0
    assert texture_coords[ 2 ][ 0 ] == 0.5
    assert texture_coords[ 2 ][ 1 ] == 0.5

