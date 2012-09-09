'''
Provides common GL functionality.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

from contextlib import contextmanager

from pyglet.gl import *

from pyrr import rectangle


def set_viewport( rect ):
    """Calls glViewport with the dimensions of
    the rectangle

    This call can be undone by first calling
    glPushAttrib( GL_VIEWPORT_BIT )
    and later calling glPopAttrib().
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
    """
    glScissor(
        int(rect[ (0,0) ]),
        int(rect[ (0,1) ]),
        int(rect[ (1,0) ]),
        int(rect[ (1,1) ])
        )

@contextmanager
def attributes( attributes ):
    """Wraps glPushAttrib and glPopAttrib
    in a context manager, providing the 'with'
    keyword.

    For example:
    with gl.attributes( GL_VIEWPORT_BIT ):
        glViewport( 0, 0, 100, 100 )
    """
    glPushAttrib( attributes )
    yield
    glPopAttrib()

@contextmanager
def begin( mode ):
    """Wraps glBegin and glEnd in a
    context manager, providing the 'with'
    keyword.

    For example:
    with gl.begin( GL_TRIANGLES ):
        glVertex2f( 0.0, 0.0 )
        glVertex2f( 0.5, 1.0 )
        glVertex2f( 1.0, 0.0 )
    """
    glBegin( mode )
    yield
    glEnd()


