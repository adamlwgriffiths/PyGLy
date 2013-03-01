"""Provides OpenGL functionality that is common
to both Core and Legacy profiles.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

from OpenGL import GL

def string_to_type( type ):
    return getattr( GL, type )

def type_to_string( glType ):
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
