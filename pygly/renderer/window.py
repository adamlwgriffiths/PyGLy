'''
Created on 02/03/2012

@author: adam
'''

from pyglet.gl import *

from viewport import Viewport


def clearColourAndDepth():
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def render( window, viewports ):
    # set ourself as the active window
    window.switch_to()

    # clear the screen
    # we'll get the viewports to clear the depth buffers
    glClear( GL_COLOR_BUFFER_BIT )

    for viewport in viewports:
        viewport.switch_to( window )
        viewport.clear(
            window,
            values = GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT 
            )
        viewport.apply_view_matrix( window )
        viewport.setup_viewport()
        viewport.render( window )
        viewport.tear_down_viewport()

