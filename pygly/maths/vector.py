'''
Created on 30/05/2011

@author: adam
'''

import numpy


def zeros():
    return numpy.zeros( 3, dtype = float )

def normalise( vec ):
    """
    Normalises a vector or a list of vectors to unit length.
    The value will be changed in place. The return value
    is for convenience.

    @param vec: a 1d array with 3 elements (a vector)
    (eg. numpy.array([ x, y, z ]) or a Nx3 array
    (eg. numpy.array([ [x1, y1, z1], [x2, y2, z2] ]).
    @return the normalised value
    """
    if vec.ndim > 1:
        # list of vectors
        lengths = numpy.apply_along_axis( numpy.linalg.norm, 1, vec )
        vec /= lengths.reshape( (-1, 1) )
        return vec
    else:
        # single vector
        vec /= numpy.linalg.norm( vec )
        return vec

def length( vec ):
    """
    Returns the length of a vector or a list of vectors

    @param vec: a 1d array with 3 elements (a vector)
    (eg. numpy.array([ x, y, z ]) or a Nx3 array
    (eg. numpy.array([ [x1, y1, z1], [x2, y2, z2] ]).
    @return The length of the vectors.
    If a 1d array was passed, it will be an integer.
    If a 2d array was passed, it will be a list.
    """
    if vec.ndim > 1:
        # list of vectors
        lengths = numpy.apply_along_axis( numpy.linalg.norm, 1, vec )
        return lengths.reshape( (-1, 1) )
    else:
        # single vector
        return numpy.linalg.norm( vec )

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

def interpolate( v1, v2, delta ):
    """
    Interpolates between 2 arrays of vectors (shape = N,3)
    by the specified delta (0.0 <= delta <= 1.0).
    """
    # scale the difference based on the time
    # we must do it this 'unreadable' way to avoid
    # loss of precision.
    # the 'readable' method (f_now = f_0 + (f1 - f0) * delta)
    # causes floating point errors due to the small values used
    # in md2 files and the values become corrupted.
    # this horrible code curtousey of this comment:
    # http://stackoverflow.com/questions/5448322/temporal-interpolation-in-numpy-matplotlib
    t = delta
    t0 = 0.0
    t1 = 1.0
    delta_t = t1 - t0
    return (t1 - t) / delta_t * v1 + (t - t0) / delta_t * v2


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
    normalise( vecs )
    print "output %s" % str(vecs)
    
    for vec in vecs:
        print "vec %s" % str(vec)
        vecLength = math.sqrt( vec[ 0 ]**2 + vec[ 1 ]**2 + vec[ 2 ]**2 )
        print vecLength
        assert vecLength == 1.0
        
        # individual length calc
        assert length( vec ) == 1.0
    
    # group length calc
    lengths = length( vecs )
    for value in lengths:
        assert value == 1.0
    
    vec = numpy.array([ 1.0, 1.0, 1.0 ])
    normalise( vec )
    value = length( vec )
    assert value == 1.0


