'''
Provides common GL functionality.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

from pyglet.gl import *

from pyrr import rectangle


def set_viewport( rect ):
    """Calls glViewport with the dimensions of
    the rectangle
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
    """
    glScissor(
        int(rect[ (0,0) ]),
        int(rect[ (0,1) ]),
        int(rect[ (1,0) ]),
        int(rect[ (1,1) ])
        )

