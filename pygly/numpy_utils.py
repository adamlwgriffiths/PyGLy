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
    Ie::

        >>> a = numpy.dtype([
        ...         ('position',    'float32',  (3,)),
        ...         ('colour',      'float32',  (3,)),
        ...         ])
        >>> numpy_utils.dtype_element_count( a )
        6
        >>> numpy_utils.dtype_element_count( a['position'] )
        3
        >>> numpy_utils.dtype_element_count( a, 'position' )
        3
    """
    def count( descr ):
        if len( descr ) > 2:
            shape = descr[ 2 ]
            # multiply the shape
            return reduce( lambda x, y: x * y, shape )
        else:
            return 1

    if name:
        shape = dtype[ name ].shape
    else:
        shape = dtype.shape

    if len(shape) > 0:
        return reduce( lambda x, y: x * y, shape )
    else:
        descr = dtype.descr
        size = 0
        for type in descr:
            size += count( type )
        return size

def dtype_type( dtype, name = None ):
    """Returns the type that compose a dtype.

    If you need the type of a specifically named
    column, pass the root dtype in with the name.
    Ie::

        type = dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
        extract_type( type, 'position' )
        >>> '<f4'
        type
        >>> dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
        type.descr
        >>> [('position', '<f4', (3,)), ('colour', '<f4', (3,))]

    Do NOT pass a subdtype or the count will be wrong.
    Ie::

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
    Ie::

        type = dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
        gl_enum( type, 'position' )
        >>> GL_FLOAT
        type
        >>> dtype([('position', '<f4', (3,)), ('colour', '<f4', (3,))])
        type.descr
        >>> [('position', '<f4', (3,)), ('colour', '<f4', (3,))]

    Do NOT pass a subdtype or the count will be wrong.
    Ie::

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
    type_ = dtype_type( dtype, name )
    stripped_type = re.sub('[=<>|]', '', type_)

    types = {
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
    }

    if stripped_type not in types:
        raise ValueError('Cannot convert from {0}'.format(type_))

    return types[ stripped_type ]

def gl_enum_dtype(enum, name=None):
    from OpenGL import GL

    types = {
        GL.GL_BYTE:             'int8',
        GL.GL_UNSIGNED_BYTE:    'uint8',
        GL.GL_SHORT:            'int16',
        GL.GL_UNSIGNED_SHORT:   'uint16',
        GL.GL_INT:              'int32',
        GL.GL_UNSIGNED_INT:     'uint32',
        GL.GL_FLOAT:            'float32',
        GL.GL_DOUBLE:           'float64',
    }
    return types[enum]

