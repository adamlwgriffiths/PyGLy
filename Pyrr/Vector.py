'''
Created on 30/05/2011

@author: adam
'''

import numpy


VecX = 0
VecY = 1
VecZ = 2

def setup():
    return numpy.zeros( 3, dtype = float )

def normalise( vector ):
    # single vector
    vector /= numpy.linalg.norm( vector )
    return vector

def normaliseList( list ):
    """
    @param a: a 1d array with 3 elements (a vector) (eg. numpy.array([ x, y, z ]) or a
    Nx3 array (eg. numpy.array([ [x1, y1, z1], [x2, y2, z2] ]).
    @return the normalised value
    """
    # list of vectors
    lengths = numpy.apply_along_axis(numpy.linalg.norm, 1, list )
    list /= lengths.reshape( (-1, 1) )
    return list
    
def length( vector ):
    # single vector
    return numpy.linalg.norm( vector )

def lengths( list ):
    # list of vectors
    lengths = numpy.apply_along_axis( numpy.linalg.norm, 1, list )
    return lengths.reshape( (-1, 1) )

def dot( a, b, out = None ):
    """
    @param a: a 1d array with 3 elements (a vector) (eg. numpy.array([ x, y, z ]) or a
    Nx3 array (eg. numpy.array([ [x1, y1, z1], [x2, y2, z2] ])
    @param b: a 1d array with 3 elements (a vector)
    @param out: a contiguous array with enough room  for the result.
    If the array is not contiguous (a column from a 2d array) it will throw an
    exception. Work around this by creating a contiguous array of a different
    shape and then reshaping, re-arranging or transposing.
    """
    return numpy.dot( a, b, out = out )

def cross( vector1, vector2 ):
    """
    @param vector1: a 1d array with 3 elements (a vector)
    @param vector2: a 1d array with 3 elements (a vector)
    """
    return numpy.cross( vector1, vector2 )


if __name__ == "__main__":
    import math
    
    print "Normalise vectors"
    vector = numpy.array( [ 1.0, 1.0, 1.0 ], dtype = float )
    normalise( vector )
    vecLength = math.sqrt( vector[ 0 ]**2 + vector[ 1 ]**2 + vector[ 2 ]**2 )
    assert vecLength == 1.0
    # individual length calc
    assert length( vector ) == 1.0
    
    # list of vectors
    vectors = numpy.array([
        [ 1.0, 1.0, 1.0 ],
        [ 0.0, 2.0, 0.0 ]
        ])
    print "input %s" % str(vectors)
    normaliseList( vectors )
    print "output %s" % str(vectors)
    
    for vector in vectors:
        print "vector %s" % str(vector)
        vecLength = math.sqrt( vector[ 0 ]**2 + vector[ 1 ]**2 + vector[ 2 ]**2 )
        print vecLength
        assert vecLength == 1.0
        
        # individual length calc
        assert length( vector ) == 1.0
    
    # group length calc
    lengths = lengths( vectors )
    for value in lengths:
        assert value == 1.0
    
    vector = numpy.array([ 1.0, 1.0, 1.0 ])
    normalise( vector )
    value = length( vector )
    assert value == 1.0


