'''
Created on 29/06/2011

@author: adam
'''

from pyglet.gl import *
from pyglet.graphics import Batch


batch = None

def initialise():
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
                # red
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                # yellow
                1.0, 1.0, 0.0,
                1.0, 1.0, 0.0,
                1.0, 1.0, 0.0,
                1.0, 1.0, 0.0,
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
                )
            )
        )

def render():
    global batch

    if batch == None:
        initialise()

    # enable back face culling
    glPushAttrib( GL_ALL_ATTRIB_BITS )
    glEnable( GL_CULL_FACE )
    glCullFace( GL_BACK )

    batch.draw()

    glPopAttrib()

