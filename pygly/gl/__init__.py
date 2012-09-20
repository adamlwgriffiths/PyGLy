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

