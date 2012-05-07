'''
Created on 02/03/2012

@author: adam
'''

import numpy
from pyglet.gl import *

from pyrr import rectangle
from pygly.renderer.viewport import Viewport


def window_size_as_rect( window ):
    return rectangle.create_from_bounds(
        left = 0,
        right = window.width,
        bottom = 0,
        top = window.height,
        data_type = numpy.int
        )

def find_viewport_for_point( window, viewports, point ):
    """
    @param window: The window the point is from.
    @param viewports: A sorted array of viewports. The first
    viewport that the point is within will be used.
    @param point: The point we are finding a viewport for.
    @return The viewport the point is within. None is returned
    if the point is not within a viewport.
    """
    for viewport in viewports:
        if viewport.is_window_point_within_viewport( point ):
            # the point is within this viewport
            return viewport

    # the point matches no viewports
    return None

def window_point_to_viewport_point( window, viewport, point ):
    """
    Converts a point relative to the window, to a point
    relative to the viewport.

    @param window: The window that contains the viewport
    and point.
    @param viewport: The viewport the point is within.
    @param point: The point on the window. This is in pixels.
    @return: The point within the viewport.
    """
    # convert to viewport co-ordinates
    relative_point = rectangle.make_point_relative(
        point,
        viewport.rect
        )

    return relative_point

def set_viewport_to_window( window ):
    """
    Calls glViewport with the dimensions of
    the window.

    This can be used to undo the call
    viewport.switch_to or glViewport.
    """
    glViewport( 0, 0, window.width, window.height )

def scissor_to_rect( rect ):
    """
    Calls glScissor with the size of the rectangle.

    It is up to the user to call
    glEnable(GL_SCISSOR_TEST).

    To undo this, use scissor_to_window.
    """
    glViewport(
        int(rect[ (0,0) ]),
        int(rect[ (0,1) ]),
        int(rect[ (1,0) ]),
        int(rect[ (1,1) ])
        )

def scissor_to_window( window ):
    glScissor( 0, 0, window.width, window.height )

def render( window, viewports ):
    # set ourself as the active window
    window.switch_to()

    # don't clear the screen incase there are
    # more viewports than just these

    # iterate through all of our viewports
    for viewport in viewports:
        # activate the viewport
        viewport.switch_to()

        # setup our open gl state for the viewport
        # also calls glScissor to the viewports dimensions
        viewport.push_viewport_attributes()

        # clear the existing depth buffer
        # we need to do this incase the viewports
        # overlap
        viewport.clear(
            values = GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT 
            )

        # apply the cameras projection matrix
        viewport.push_view_matrix()
        # apply the cameras model view
        viewport.push_model_view()
        # render the scene
        viewport.render( window )
        # undo our camera model view
        viewport.pop_model_view()
        # undo our camera projection matrix
        viewport.pop_view_matrix()

        # undo any opengl state we set for the viewport
        viewport.pop_viewport_attributes()

    # reset the viewport to the full window
    set_viewport_to_window( window )

    # undo any viewport scissor calls
    scissor_to_window( window )

    # set matrix back to model view just incase
    # the last call was to pop_view_matrix which
    # sets it to GL_PROJECTION
    glMatrixMode( GL_MODELVIEW )

