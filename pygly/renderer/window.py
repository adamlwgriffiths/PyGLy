'''
Created on 02/03/2012

@author: adam
'''

from pyglet.gl import *

from viewport import Viewport


def render( window, viewports ):
    # set ourself as the active window
    window.switch_to()

    # clear the screen
    # we'll get the viewports to clear the depth buffers
    glClear( GL_COLOR_BUFFER_BIT )

    for viewport in viewports:
        # activate the viewport
        viewport.switch_to( window )

        # clear the existing depth buffer
        # we need to do this incase the viewports
        # overlap
        viewport.clear(
            window,
            values = GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT 
            )

        # apply the cameras projection matrix
        viewport.apply_view_matrix()
        # apply the cameras model view
        viewport.apply_model_view()
        # setup our open gl state for the viewport
        viewport.setup_viewport()
        # render the scene
        viewport.render( window )
        # undo any opengl state we set for the viewport
        viewport.tear_down_viewport()

