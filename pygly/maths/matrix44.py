'''
Created on 23/06/2011

@author: adam
'''

import math

import numpy

import maths.matrix33


def identity( out = None ):
    if out == None:
        out = numpy.empty( (4, 4), dtype = float )
    
    out[:] = [
        [ 1.0, 0.0, 0.0, 0.0 ],
        [ 0.0, 1.0, 0.0, 0.0 ],
        [ 0.0, 0.0, 1.0, 0.0 ],
        [ 0.0, 0.0, 0.0, 1.0 ]
        ]
    return out

def setup( eulers, out = None ):
    """
    Proper matrix layout and layout used for DirectX.
    For OpenGL, transpose the matrix after calling this.
    """
    # set to identity matrix
    # this will populate our extra rows for us
    out = identity( out )
    
    # we'll use Matrix33 for our conversion
    mat33 = out[ 0:3, 0:3 ]
    mat33 = maths.matrix33.setup( eulers, out = mat33 )
    
    return out

def from_inertial_to_object_quaternion( quat, out = None ):
    """
    Proper matrix layout and layout used for DirectX.
    For OpenGL, transpose the matrix after calling this.
    """
    # set to identity matrix
    # this will populate our extra rows for us
    out = identity( out )
    
    # we'll use Matrix33 for our conversion
    mat33 = out[ 0:3, 0:3 ]
    maths.matrix33.from_inertial_to_object_quaternion( quat, out = mat33 )
    
    return out

def from_object_to_inertial_quaternion( quat, out = None ):
    """
    Proper matrix layout and layout used for DirectX.
    For OpenGL, transpose the matrix after calling this.
    """
    # set to identity matrix
    # this will populate our extra rows for us
    out = identity( out )
    
    # we'll use Matrix33 for our conversion
    mat33 = out[ 0:3, 0:3 ]
    maths.matrix33.from_object_to_inertial_quaternion( quat, out = mat33 )
    
    return out

def inertial_to_object( vector, matrix, out = None ):
    """
    Proper matrix layout and layout used for DirectX.
    For OpenGL, transpose the matrix after calling this.
    """
    # set to identity matrix
    # this will populate our extra rows for us
    out = identity( out )
    
    # we'll use Matrix33 for our conversion
    mat33 = out[ 0:3, 0:3 ]
    maths.matrix33.inertial_to_object( vector, out = mat33 )
    
    return out

def multiply( m1, m2, out = None ):
    if out == None:
        out = numpy.empty( (4, 4), dtype = float )
    out[:] = numpy.dot( m1, m2 )
    return out

def set_translation( matrix, vector, out = None ):
    if out == None:
        out = numpy.empty( (4, 4), dtype = float )
    
    out[:] = matrix
    # apply the vector to the first 3 values of the last row
    out[ 3, 0:3 ] = vector
    
    return out

def scale( matrix, scale, out = None ):
    if out == None:
        out = identity() 
    
    scale_matrix = identity()
    # apply the scale to the values diagonally
    # down the matrix
    scale_matrix[ 0,0 ] *= scale[ 0 ]
    scale_matrix[ 1,1 ] *= scale[ 1 ]
    scale_matrix[ 2,2 ] *= scale[ 2 ]

    multiply( matrix, scale_matrix, out = out )
    
    return out

if __name__ == "__main__":
    mat44 = identity()
    # TODO: add more tests
    
    eulers = numpy.array( [ 1.0, 2.0, 0.5 ], dtype = float )
    setup( eulers, out = mat44 )
    assert mat44[ 3, 3 ] == 1.0
    
    out = numpy.empty( (4, 4), dtype = float )
    set_translation( mat44, [ 1.0, 2.0, 3.0 ], out )
    # translation goes down the last column in normal matrix
    # opengl uses a transposed matrix
    assert out[ 3 ][ 0 ] == 1.0
    assert out[ 3 ][ 1 ] == 2.0
    assert out[ 3 ][ 2 ] == 3.0
    assert out is not mat44

