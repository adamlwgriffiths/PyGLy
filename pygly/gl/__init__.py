"""Provides OpenGL functionality that is common
to both Core and Legacy profiles.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

from contextlib import contextmanager
from ctypes import string_at

from pyglet.gl import *


def set_viewport( rect ):
    """Calls glViewport with the dimensions of
    the rectangle

    This call can be undone by first calling
    glPushAttrib( GL_VIEWPORT_BIT )
    and later calling glPopAttrib().

    Or using the attribute context:
    with attributes( GL_VIEWPORT_BIT ):
        set_viewport( rect )
    """
    glViewport(
        int(rect[ 0 ][ 0 ]),
        int(rect[ 0 ][ 1 ]),
        int(rect[ 1 ][ 0 ]),
        int(rect[ 1 ][ 1 ])
        )

def set_scissor( rect ):
    """Calls glScissor with the size of the rectangle.

    .. note:: It is up to the user to call glEnable(GL_SCISSOR_TEST).

    .. note:: To undo this, call this function again with the window's size as a rectangle.

    .. seealso::
        Module :py:mod:`pygly.window`
          Documentation of the :py:mod:`pygly.window` module.

    This call can be undone by first calling
    glPushAttrib( GL_SCISSOR_BIT )
    and later calling glPopAttrib().

    Or using the attribute context:
    with attributes( GL_SCISSOR_BIT ):
        set_scissor( rect )
    """
    glScissor(
        int(rect[ 0 ][ 0 ]),
        int(rect[ 0 ][ 1 ]),
        int(rect[ 1 ][ 0 ]),
        int(rect[ 1 ][ 1 ])
        )

def gl_version():
    return gl_info.get_version()

def is_legacy():
    return gl_info.have_version( major = 1 )

def is_core():
    return gl_info.have_version( major = 3 )

def glsl_version():
    return string_at(
        glGetString( GL_SHADING_LANGUAGE_VERSION )
        )

def print_gl_info():
    print "OpenGL version:", gl_info.get_version()
    print "GLSL version:", glsl_version()

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

def enum_to_string( glEnum ):
    return {
        GL_FLOAT:               "GL_FLOAT",
        GL_FLOAT_VEC2:          "GL_FLOAT_VEC2",
        GL_FLOAT_VEC3:          "GL_FLOAT_VEC3",
        GL_FLOAT_VEC4:          "GL_FLOAT_VEC4",
        GL_INT:                 "GL_INT",
        GL_INT_VEC2:            "GL_INT_VEC2",
        GL_INT_VEC3:            "GL_INT_VEC3",
        GL_INT_VEC4:            "GL_INT_VEC4",
        GL_UNSIGNED_INT:        "GL_UNSIGNED_INT",
        GL_UNSIGNED_INT_VEC2:   "GL_UNSIGNED_INT_VEC2",
        GL_UNSIGNED_INT_VEC3:   "GL_UNSIGNED_INT_VEC3",
        GL_UNSIGNED_INT_VEC4:   "GL_UNSIGNED_INT_VEC4",
        GL_UNSIGNED_INT_ATOMIC_COUNTER: "GL_UNSIGNED_INT_ATOMIC_COUNTER",
        GL_FLOAT_MAT2:          "GL_FLOAT_MAT2",
        GL_FLOAT_MAT3:          "GL_FLOAT_MAT3",
        GL_FLOAT_MAT4:          "GL_FLOAT_MAT4",
        GL_FLOAT_MAT2x3:        "GL_FLOAT_MAT2x3",
        GL_FLOAT_MAT2x4:        "GL_FLOAT_MAT2x4",
        GL_FLOAT_MAT3x2:        "GL_FLOAT_MAT3x2",
        GL_FLOAT_MAT3x4:        "GL_FLOAT_MAT3x4",
        GL_FLOAT_MAT4x2:        "GL_FLOAT_MAT4x2",
        GL_FLOAT_MAT4x3:        "GL_FLOAT_MAT4x3",
        GL_SAMPLER_1D:          "GL_SAMPLER_1D",
        GL_SAMPLER_2D:          "GL_SAMPLER_2D",
        GL_SAMPLER_3D:          "GL_SAMPLER_3D",
        GL_SAMPLER_CUBE:        "GL_SAMPLER_CUBE",
        GL_SAMPLER_1D_SHADOW:   "GL_SAMPLER_1D_SHADOW",
        GL_SAMPLER_2D_SHADOW:   "GL_SAMPLER_2D_SHADOW",
        GL_SAMPLER_1D_ARRAY:    "GL_SAMPLER_1D_ARRAY",
        GL_SAMPLER_2D_ARRAY:    "GL_SAMPLER_2D_ARRAY",
        GL_SAMPLER_1D_ARRAY_SHADOW: "GL_SAMPLER_1D_ARRAY_SHADOW",
        GL_SAMPLER_2D_ARRAY_SHADOW: "GL_SAMPLER_2D_ARRAY_SHADOW",
        GL_SAMPLER_2D_MULTISAMPLE:  "GL_SAMPLER_2D_MULTISAMPLE",
        GL_SAMPLER_2D_MULTISAMPLE_ARRAY:    "GL_SAMPLER_2D_MULTISAMPLE_ARRAY",
        GL_SAMPLER_CUBE_SHADOW: "GL_SAMPLER_CUBE_SHADOW",
        GL_SAMPLER_BUFFER:      "GL_SAMPLER_BUFFER",
        GL_SAMPLER_2D_RECT:     "GL_SAMPLER_2D_RECT",
        GL_SAMPLER_2D_RECT_SHADOW:  "GL_SAMPLER_2D_RECT_SHADOW",
        GL_INT_SAMPLER_1D:      "GL_INT_SAMPLER_1D",
        GL_INT_SAMPLER_2D:      "GL_INT_SAMPLER_2D",
        GL_INT_SAMPLER_3D:      "GL_INT_SAMPLER_3D",
        GL_INT_SAMPLER_CUBE:    "GL_INT_SAMPLER_CUBE",
        GL_INT_SAMPLER_1D_ARRAY:    "GL_INT_SAMPLER_1D_ARRAY",
        GL_INT_SAMPLER_2D_ARRAY:    "GL_INT_SAMPLER_2D_ARRAY",
        GL_INT_SAMPLER_2D_MULTISAMPLE:  "GL_INT_SAMPLER_2D_MULTISAMPLE",
        GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:    "GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
        GL_INT_SAMPLER_BUFFER:  "GL_INT_SAMPLER_BUFFER",
        GL_INT_SAMPLER_2D_RECT: "GL_INT_SAMPLER_2D_RECT",
        GL_UNSIGNED_INT_SAMPLER_1D: "GL_UNSIGNED_INT_SAMPLER_1D",
        GL_UNSIGNED_INT_SAMPLER_2D: "GL_UNSIGNED_INT_SAMPLER_2D",
        GL_UNSIGNED_INT_SAMPLER_3D: "GL_UNSIGNED_INT_SAMPLER_3D",
        GL_UNSIGNED_INT_SAMPLER_CUBE:   "GL_UNSIGNED_INT_SAMPLER_CUBE",
        GL_UNSIGNED_INT_SAMPLER_1D_ARRAY:   "GL_UNSIGNED_INT_SAMPLER_1D_ARRAY",
        GL_UNSIGNED_INT_SAMPLER_2D_ARRAY:   "GL_UNSIGNED_INT_SAMPLER_2D_ARRAY",
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE",
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:   "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
        GL_UNSIGNED_INT_SAMPLER_BUFFER: "GL_UNSIGNED_INT_SAMPLER_BUFFER",
        GL_UNSIGNED_INT_SAMPLER_2D_RECT:    "GL_UNSIGNED_INT_SAMPLER_2D_RECT",
        GL_IMAGE_1D:            "GL_IMAGE_1D",
        GL_IMAGE_2D:            "GL_IMAGE_2D",
        GL_IMAGE_3D:            "GL_IMAGE_3D",
        GL_IMAGE_2D_RECT:       "GL_IMAGE_2D_RECT",
        GL_IMAGE_CUBE:          "GL_IMAGE_CUBE",
        GL_IMAGE_BUFFER:        "GL_IMAGE_BUFFER",
        GL_IMAGE_1D_ARRAY:      "GL_IMAGE_1D_ARRAY",
        GL_IMAGE_2D_ARRAY:      "GL_IMAGE_2D_ARRAY",
        GL_IMAGE_2D_MULTISAMPLE:    "GL_IMAGE_2D_MULTISAMPLE",
        GL_IMAGE_2D_MULTISAMPLE_ARRAY:  "GL_IMAGE_2D_MULTISAMPLE_ARRAY",
        GL_INT_IMAGE_1D:        "GL_INT_IMAGE_1D",
        GL_INT_IMAGE_2D:        "GL_INT_IMAGE_2D",
        GL_INT_IMAGE_3D:        "GL_INT_IMAGE_3D",
        GL_INT_IMAGE_2D_RECT:   "GL_INT_IMAGE_2D_RECT",
        GL_INT_IMAGE_CUBE:      "GL_INT_IMAGE_CUBE",
        GL_INT_IMAGE_BUFFER:    "GL_INT_IMAGE_BUFFER",
        GL_INT_IMAGE_1D_ARRAY:  "GL_INT_IMAGE_1D_ARRAY",
        GL_INT_IMAGE_2D_ARRAY:  "GL_INT_IMAGE_2D_ARRAY",
        GL_INT_IMAGE_2D_MULTISAMPLE:    "GL_INT_IMAGE_2D_MULTISAMPLE",
        GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY:  "GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY",
        GL_UNSIGNED_INT_IMAGE_1D:   "GL_UNSIGNED_INT_IMAGE_1D",
        GL_UNSIGNED_INT_IMAGE_2D:   "GL_UNSIGNED_INT_IMAGE_2D",
        GL_UNSIGNED_INT_IMAGE_3D:   "GL_UNSIGNED_INT_IMAGE_3D",
        GL_UNSIGNED_INT_IMAGE_2D_RECT:  "GL_UNSIGNED_INT_IMAGE_2D_RECT",
        GL_UNSIGNED_INT_IMAGE_CUBE: "GL_UNSIGNED_INT_IMAGE_CUBE",
        GL_UNSIGNED_INT_IMAGE_BUFFER:   "GL_UNSIGNED_INT_IMAGE_BUFFER",
        GL_UNSIGNED_INT_IMAGE_1D_ARRAY: "GL_UNSIGNED_INT_IMAGE_1D_ARRAY",
        GL_UNSIGNED_INT_IMAGE_2D_ARRAY: "GL_UNSIGNED_INT_IMAGE_2D_ARRAY",
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE:   "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE",
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY: "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY",
        }[ glEnum ]

