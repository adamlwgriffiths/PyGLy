'''
Created on 07/06/2012

@author: adam
'''

import numpy

def sort_front_to_back(
    render_position,
    render_direction,
    objects,
    object_positions
    ):
    if len( object_positions ) <= 0:
        return numpy.empty( 0 )

    # make positions relative to render position
    relative_positions = object_positions - render_position

    # do a dot product against the render direction
    dot_values = numpy.apply_along_axis(
        numpy.dot,
        relative_positions.ndim - 1,
        relative_positions,
        render_direction
        )

    # sort the object array by the
    # dot product of the object positions
    # sort in ascending order

    # this first call sorts and returns the indices
    inds = numpy.argsort( dot_values, axis = -1 )

    # we then rebuilt the object array by the indices
    sorted_objects = numpy.take( objects, inds )

    return sorted_objects

def sort_back_to_front(
    render_position,
    render_direction,
    objects,
    object_positions
    ):
    # sort front to back
    sorted_objects = sort_front_to_back(
        render_position,
        render_direction,
        objects,
        object_positions
        )

    # reverse the array
    return sorted_objects[::-1]

