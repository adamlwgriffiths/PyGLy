'''
Created on 07/06/2012

@author: adam
'''

import numpy

import pyrr

def sort_plane_front_to_back(
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
    dot_values = pyrr.vector.dot(
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

def sort_plane_back_to_front(
    render_position,
    render_direction,
    objects,
    object_positions
    ):
    # sort front to back
    sorted_objects = sort_plane_front_to_back(
        render_position,
        render_direction,
        objects,
        object_positions
        )

    # reverse the array
    return sorted_objects[::-1]

def sort_radius_front_to_back(
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
    lengths = pyrr.vector.squared_length(
        relative_positions
        )

    # sort the object array by the
    # dot product of the object positions
    # sort in ascending order

    # this first call sorts and returns the indices
    inds = numpy.argsort( lengths, axis = -1 )

    # we then rebuilt the object array by the indices
    sorted_objects = numpy.take( objects, inds )

    # return inverted
    return sorted_objects

def sort_radius_back_to_front(
    render_position,
    render_direction,
    objects,
    object_positions
    ):
    # sort front to back
    sorted_objects = sort_radius_front_to_back(
        render_position,
        render_direction,
        objects,
        object_positions
        )

    # reverse the array
    return sorted_objects[::-1]

