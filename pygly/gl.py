'''
Created on 22/05/2012

@author: adam
'''

from pyglet.gl import *

from pyrr import rectangle


def set_viewport( rect ):
    """
    Calls glViewport with the dimensions of
    the window.

    This can be used to undo the call
    viewport.switch_to or glViewport.
    """
    glViewport(
        int(rect[ 0 ][ 0 ]),
        int(rect[ 0 ][ 1 ]),
        int(rect[ 1 ][ 0 ]),
        int(rect[ 1 ][ 1 ])
        )

def set_scissor( rect ):
    """
    Calls glScissor with the size of the rectangle.

    It is up to the user to call
    glEnable(GL_SCISSOR_TEST).

    To undo this, use scissor_to_window.
    """
    glScissor(
        int(rect[ (0,0) ]),
        int(rect[ (0,1) ]),
        int(rect[ (1,0) ]),
        int(rect[ (1,1) ])
        )

