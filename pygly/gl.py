"""Common and helpful OpenGL functions.

Becareful when using contextmanager aware functions such as load_matrix, etc.
Python supports using multiple contextmanager functions in a single statement.
However, you should **NOT** do this.
When python unwinds the contextmanagers, it does so in the same order it
set them, not the reverse order.

For example::

    with matrix_mode( GL_PROJECTION ), load_matrix( mat ):
        pass

This code *looks* innocuous. However, Python will call the functions in the
following order::

    # winding
    matrix_mode( GL_PROJECTION )
    load_matrix( mat )
    # code goes here

    # unwinding
    matrix_mode( GL_PROJECTION )
    load_matrix( mat )

As you can see, when unwinding the functions, Python popped the matrix mode
and then popped the matrix.
"""
from contextlib import contextmanager

import numpy
from OpenGL import GL

from pyrr.utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


def _generate_enum_map( enum_names ):
    """Convert dicts of format {'GL_ENUM_NAME': value, ...}
    to { GL_ENUM_NAME : value, ...}

    Used to ignore NameErrors that would otherwise result from incomplete
    OpenGL implementations.
    """
    map = {}
    for (key, value) in enum_names.items():
        try:
            map[ getattr(GL, key) ] = value
        except AttributeError:
            pass
    return map

def _extract_version(version):
    """Extracts the major and minor versions from an OpenGL version string.

    Can handle driver's appending their specific driver version to the string.
    """
    import re
    # version is guaranteed to be 'MAJOR.MINOR<XXX>'
    # there can be a 3rd version
    # split full stops and spaces and take the first 2 results
    versions = re.split( r'[\.\s\-]', version )
    return int(versions[0]), int(versions[1])

def gl_version():
    """Returns the current OpenGL version string as specified by the
    OpenGL drivers.
    """
    return GL.glGetString( GL.GL_VERSION )

def gl_version_tuple():
    return _extract_version( gl_version() )

def gl_profile():
    """Determines the current OpenGL profile version.

    :rtype: string
    :return: Returns 'legacy' or 'core' depending on the current OpenGL version.
    """
    major, minor = gl_version_tuple()
    if major <= 2:
        return 'legacy'
    else:
        return 'core'

def glsl_version():
    """Returns the GLSL version string.
    """
    return GL.glGetString( GL.GL_SHADING_LANGUAGE_VERSION )

def glsl_version_tuple():
    """Returns the GLSL version as a tuple.

    :rtype: tuple
    :return: The major and minor version strings as a tuple (major, minor).
    """
    return _extract_version( glsl_version() )

def is_legacy():
    """Checks if the OpenGL version is using the Legacy profile.

    :rtype: boolean
    :return: True if the OpenGL major version is <= 2.
    """
    return gl_version_tuple()[ 0 ] <= 2

def is_core():
    """Checks if the OpenGL version is using the Core profile.

    :rtype: boolean
    :return: True if the OpenGL major version is >= 3.
    """
    return gl_version_tuple()[ 0 ] >= 3

def print_gl_info():
    """Prints common OpenGL version information.
    """
    print "OpenGL Information:"
    for prop in ["GL_VENDOR", "GL_RENDERER", "GL_VERSION", "GL_SHADING_LANGUAGE_VERSION"]:
        type = getattr( GL, prop )
        value = GL.glGetString( type )
        print "\t%s = %s" % (prop, value)

def string_to_type( type ):
    """Converts an OpenGL type from a string to an actual type.

    Not all OpenGL types will be supported by this function.

    :param type: The OpenGL type as a string.
    :return: The primitive type.
    """
    return getattr( GL, type )

def type_to_string( glType ):
    """Converts OpenGL primitive types to a string.

    :param glType: The primitive type.
        Supports the following values::

            GLbyte
            GLubyte
            GLshort
            GLushort
            GLint
            GLuint
            GLfloat
            GLdouble

    :rtype: string
    :return: A string representing the specified OpenGL primitive type.
    """
    return {
        GL.GLbyte:     "GLbyte",
        GL.GLubyte:    "GLubyte",
        GL.GLshort:    "GLshort",
        GL.GLushort:   "GLushort",
        GL.GLint:      "GLint",
        GL.GLuint:     "GLuint",
        GL.GLfloat:    "GLfloat",
        GL.GLdouble:   "GLdouble",
        }[ glType ]

def enum_to_type( glEnum ):
    return {
        GL.constants.GL_CHAR:           GL.constants.GLchar,
        GL.constants.GL_UNSIGNED_BYTE:  GL.constants.GLubyte,
        GL.constants.GL_BYTE:           GL.constants.GLbyte,
        GL.constants.GL_UNSIGNED_SHORT: GL.constants.GLushort,
        GL.constants.GL_SHORT:          GL.constants.GLshort,
        GL.constants.GL_UNSIGNED_INT:   GL.constants.GLuint,
        GL.constants.GL_INT:            GL.constants.GLint,
        GL.constants.GL_FLOAT:          GL.constants.GLfloat,
        GL.constants.GL_DOUBLE:         GL.constants.GLdouble,
        }[ glEnum ]

@contextmanager
def attributes( attribs ):
    """Wraps glPushAttrib and glPopAttrib
    in a context manager, providing the 'with'
    keyword.

    For example::

        with attributes( GL_VIEWPORT_BIT ):
            glViewport( 0, 0, 100, 100 )

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPushAttrib( attribs )
    try:
        yield
    finally:
        GL.glPopAttrib()

@contextmanager
def begin( mode ):
    """Wraps glBegin and glEnd in a
    context manager, providing the 'with'
    keyword.

    For example::

        with begin( GL_TRIANGLES ):
            glVertex2f( 0.0, 0.0 )
            glVertex2f( 0.5, 1.0 )
            glVertex2f( 1.0, 0.0 )

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glBegin( mode )
    try:
        yield
    finally:
        GL.glEnd()

@contextmanager
def matrix_mode( mode ):
    """Wraps glMatrixMode in a context manager,
    providing the 'with' keyword.
    Automatically restores the existing matrix
    mode on exit.

    For example::

        with matrix_mode( GL_MODELVIEW ):
            pass

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPushAttrib( GL.GL_TRANSFORM_BIT )
    GL.glMatrixMode( mode )
    try:
        yield
    finally:
        GL.glPopAttrib()

@contextmanager
@all_parameters_as_numpy_arrays
def load_matrix( mat ):
    """Wraps glPushMatrix, glPopMatrix and
    glLoadMatrixf in a context manager,
    providing the 'with' keyword.

    Arrays will be loaded as 32-bit floats.

    For example::

        with load_matrix( world_matrix ):
            pass

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPushMatrix()
    GL.glLoadMatrixf( mat.astype('float32') )

    try:
        yield
    finally:
        GL.glPopMatrix()

@contextmanager
@all_parameters_as_numpy_arrays
def multiply_matrix( mat ):
    """Wraps glPushMatrix, glPopMatrix and
    glMultMatrixf in a context manager,
    providing the 'with' keyword.

    Arrays will be loaded as 32-bit floats.

    For example::

        with multiply_matrix( world_matrix ):
            pass

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPushMatrix()
    GL.glMultMatrixf( mat.astype('float32') )

    try:
        yield
    finally:
        GL.glPopMatrix()

@contextmanager
@parameters_as_numpy_arrays( 'mat' )
def mode_and_matrix( mode, mat ):
    """Sets the matrix mode and pushes a matrix into that mode's stack.

    This is the equivalent to::

        with matrix_mode( mode ):
            with load_matrix( mat ):
                pass

    .. warning:: This function is removed from the OpenGL Core profile and **only**
        exists in OpenGL Legacy profile (OpenGL version <=2.1).
    """
    GL.glPushAttrib( GL.GL_TRANSFORM_BIT )
    GL.glMatrixMode( mode )
    GL.glPushMatrix()
    GL.glMultMatrixf( mat.astype('float32') )
    try:
        yield
    finally:
        GL.glPopMatrix()
        GL.glPopAttrib()

