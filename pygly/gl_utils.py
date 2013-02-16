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

