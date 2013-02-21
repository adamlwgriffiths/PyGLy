"""Provides OpenGL functionality that is common
to both Core and Legacy profiles.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

from OpenGL.GL import *

def string_to_type( type ):
    return globals()[type]

def type_to_string( glType ):
    return {
        GLbyte:     "GLbyte",
        GLubyte:    "GLubyte",
        GLshort:    "GLshort",
        GLushort:   "GLushort",
        GLint:      "GLint",
        GLuint:     "GLuint",
        GLfloat:    "GLfloat",
        GLdouble:   "GLdouble",
        }[ glType ]

def numpy_dtype_to_enum( array ):
    return {
        'int8':     GL_BYTE,
        'uint8':    GL_UNSIGNED_BYTE,
        'int16':    GL_SHORT,
        'uint16':   GL_UNSIGNED_SHORT,
        'int32':    GL_INT,
        'uint32':   GL_UNSIGNED_INT,
        'float16':  GL_HALF_FLOAT,
        'float32':  GL_FLOAT,
        'float64':  GL_DOUBLE,
        }[ array.dtype ]

