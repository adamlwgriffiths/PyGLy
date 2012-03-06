'''
Created on 30/05/2011

@author: adam
'''

import numpy


x = 0
y = 1
z = 2

def setup():
    return numpy.zeros( 3, dtype = float )

def normalise( vec ):
    # single vector
    vec /= numpy.linalg.norm( vec )
    return vec

def normalise_list( list ):
    """
    @param a: a 1d array with 3 elements (a vector) (eg. numpy.array([ x, y, z ]) or a
    Nx3 array (eg. numpy.array([ [x1, y1, z1], [x2, y2, z2] ]).
    @return the normalised value
    """
    # list of vectors
    lengths = numpy.apply_along_axis( numpy.linalg.norm, 1, list )
    list /= lengths.reshape( (-1, 1) )
    return list
    
def length( vec ):
    # single vector
    return numpy.linalg.norm( vec )

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
    vec = numpy.array( [ 1.0, 1.0, 1.0 ], dtype = float )
    normalise( vec )
    vecLength = math.sqrt( vec[ 0 ]**2 + vec[ 1 ]**2 + vec[ 2 ]**2 )
    assert vecLength == 1.0
    # individual length calc
    assert length( vec ) == 1.0
    
    # list of vectors
    vecs = numpy.array([
        [ 1.0, 1.0, 1.0 ],
        [ 0.0, 2.0, 0.0 ]
        ])
    print "input %s" % str(vecs)
    normalise_list( vecs )
    print "output %s" % str(vecs)
    
    for vec in vecs:
        print "vec %s" % str(vec)
        vecLength = math.sqrt( vec[ 0 ]**2 + vec[ 1 ]**2 + vec[ 2 ]**2 )
        print vecLength
        assert vecLength == 1.0
        
        # individual length calc
        assert length( vec ) == 1.0
    
    # group length calc
    lengths = lengths( vecs )
    for value in lengths:
        assert value == 1.0
    
    vec = numpy.array([ 1.0, 1.0, 1.0 ])
    normalise( vec )
    value = length( vec )
    assert value == 1.0


