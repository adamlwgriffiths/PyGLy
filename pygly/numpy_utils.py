"""Provides utilities for processing numpy arrays.
"""

import numpy


def dtype_stride( dtype, name = None ):
    """Returns the number of bytes in a single row of the
    specified dtype.
    """
    if name:
        return dtype[ name ].itemsize
    else:
        return dtype.itemsize

def dtype_offset( dtype, name = None ):
    """Returns the initial offset of the named property.

    If no name is given, 0 is returned.

    :raise KeyError: Raised if the specified name is not found.
    """
    if name:
        # get the dtype for the named value
        # the offset is the second value
        return dtype.fields[ name ][ 1 ]
    else:
        return 0

def dtype_element_count( dtype, name = None ):
    """Returns the number of values that compose a dtype.

    If you need the number of elements of a specifically named
    column, pass the root dtype in with the name.
    Ie.

    type = dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
    num_elements( type, 'position' )
    >>> 3
    type
    >>> dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
    type.descr
    >>> [('position', '<f4', (3,)), ('colour', '<f4', (3,))]

    Do NOT pass a subdtype or the count will be wrong.
    Ie.

    numpy.dtype( [
        ('position', 'f4', (3,)).
        ('colour', 'i2', (3,))
        ])
    num_elements( dtype[ 'position' ] )
    >>> 1
    type[ 'position' ]
    >>> dtype(('float32',(3,)))
    type[ 'position' ].descr
    >>> [('', '|V12')]
    """
    def count( descr ):
        if len( descr ) > 2:
            shape = descr[ 2 ]
            # multiply the shape
            return reduce( lambda x, y: x * y, shape )
        else:
            return 1

    descr = dtype.descr

    # we've been given a name
    if name:
        # find the name in the descriptions
        for property in descr:
            if property[ 0 ] == name:
                return count( property )

        # name not found
        raise ValueError( "Property not found" )
    else:
        # no name given
        # sum the number of values for each dtype
        sum = 0
        for type in descr:
            sum += count( type )
        return sum

def dtype_type( dtype, name = None ):
    """Returns the type that compose a dtype.

    If you need the type of a specifically named
    column, pass the root dtype in with the name.
    Ie.

    type = dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
    extract_type( type, 'position' )
    >>> '<f4'
    type
    >>> dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
    type.descr
    >>> [('position', '<f4', (3,)), ('colour', '<f4', (3,))]

    Do NOT pass a subdtype or the count will be wrong.
    Ie.

    numpy.dtype( [
        ('position', 'f4', (3,)).
        ('colour', 'i2', (3,))
        ])
    num_elements( dtype[ 'position' ] )
    >>> '|V12'
    type[ 'position' ]
    >>> dtype(('float32',(3,)))
    type[ 'position' ].descr
    >>> [('', '|V12')]
    """
    if name:
        for property in dtype.descr:
            if property[ 0 ] == name:
                return property[ 1 ]
        raise ValueError( "Property not found" )
    else:
        if len( dtype.descr ) > 1:
            raise ValueError( "Multiple types present" )

        return dtype.descr[ 0 ][ 1 ]

def dtype_gl_enum( dtype, name = None ):
    """Returns the type that compose a dtype.

    If you need the type of a specifically named
    column, pass the root dtype in with the name.
    Ie.

    type = dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
    gl_enum( type, 'position' )
    >>> GL_FLOAT
    type
    >>> dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
    type.descr
    >>> [('position', '<f4', (3,)), ('colour', '<f4', (3,))]

    Do NOT pass a subdtype or the count will be wrong.
    Ie.

    numpy.dtype( [
        ('position', 'f4', (3,)).
        ('colour', 'i2', (3,))
        ])
    gl_enum( dtype[ 'position' ] )
    >>> KeyError: 'V12'
    type[ 'position' ]
    >>> dtype(('float32',(3,)))
    type[ 'position' ].descr
    >>> [('', '|V12')]
    """
    from OpenGL import GL
    import re

    # remove endian identifiers
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.dtype.byteorder.html#numpy.dtype.byteorder
    type = dtype_type( dtype, name )
    stripped_type = re.sub('[=<>|]', '', type)

    return {
        'int8':     GL.GL_BYTE,
        'i1':       GL.GL_BYTE,
        'uint8':    GL.GL_UNSIGNED_BYTE,
        'u1':       GL.GL_UNSIGNED_BYTE,
        'int16':    GL.GL_SHORT,
        'i2':       GL.GL_SHORT,
        'uint16':   GL.GL_UNSIGNED_SHORT,
        'u2':       GL.GL_UNSIGNED_SHORT,
        'int32':    GL.GL_INT,
        'i4':       GL.GL_INT,
        'uint32':   GL.GL_UNSIGNED_INT,
        'u4':       GL.GL_UNSIGNED_INT,
        'float32':  GL.GL_FLOAT,
        'f4':       GL.GL_FLOAT,
        'float64':  GL.GL_DOUBLE,
        'f8':       GL.GL_DOUBLE,
        }[ stripped_type ]

