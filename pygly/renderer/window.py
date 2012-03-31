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
        viewport.push_view_matrix()
        # apply the cameras model view
        viewport.push_model_view()
        # setup our open gl state for the viewport
        viewport.push_viewport_attributes()
        # render the scene
        viewport.render( window )
        # undo any opengl state we set for the viewport
        viewport.pop_viewport_attributes()
        # undo our camera model view
        viewport.pop_model_view()
        # undo our camera projection matrix
        viewport.pop_view_matrix()

    # set the viewport to the full window
    glViewport( 0, 0, window.width, window.height )

