'''
Renders a debug cube for visualising 3D coodinates.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

from pyglet.gl import *
from pyglet.graphics import Batch


batch = None

def initialise():
    """Initialises the cube render objects.
    """
    global batch
    batch = Batch()

    batch.add(
        24,
        GL_QUADS,
        None,
        (
            'v3f',
            (
                 1.0, 1.0,-1.0,
                -1.0, 1.0,-1.0,
                -1.0, 1.0, 1.0,
                 1.0, 1.0, 1.0,
                
                 1.0,-1.0, 1.0,
                -1.0,-1.0, 1.0,
                -1.0,-1.0,-1.0,
                 1.0,-1.0,-1.0,
                
                 1.0, 1.0, 1.0,
                -1.0, 1.0, 1.0,
                -1.0,-1.0, 1.0,
                 1.0,-1.0, 1.0,
                
                 1.0,-1.0,-1.0,
                -1.0,-1.0,-1.0,
                -1.0, 1.0,-1.0,
                 1.0, 1.0,-1.0,
                
                -1.0, 1.0, 1.0,
                -1.0, 1.0,-1.0,
                -1.0,-1.0,-1.0,
                -1.0,-1.0, 1.0,
                
                 1.0, 1.0,-1.0,
                 1.0, 1.0, 1.0,
                 1.0,-1.0, 1.0,
                 1.0,-1.0,-1.0
                )
            ),
        (
            'c3f',
            (
                # green
                0.0, 1.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 1.0, 0.0,
                # orange
                1.0, 0.5, 0.0,
                1.0, 0.5, 0.0,
                1.0, 0.5, 0.0,
                1.0, 0.5, 0.0,
                # blue
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
                # violet
                1.0, 0.0, 1.0,
                1.0, 0.0, 1.0,
                1.0, 0.0, 1.0,
                1.0, 0.0, 1.0,
                # yellow
                1.0, 1.0, 0.0,
                1.0, 1.0, 0.0,
                1.0, 1.0, 0.0,
                1.0, 1.0, 0.0,
                # red
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                )
            )
        )

def render():
    """Renders the cube.
    """
    global batch

    if batch == None:
        initialise()

    # enable back face culling
    glPushAttrib( GL_ALL_ATTRIB_BITS )
    glEnable( GL_CULL_FACE )
    glCullFace( GL_BACK )

    batch.draw()

    glPopAttrib()

