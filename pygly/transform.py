'''
Created on 11/06/2012

@author: adam
'''

import sys
import weakref

import numpy
from pyglet.event import EventDispatcher

from pyrr import quaternion
from pyrr import matrix33
from pyrr import matrix44

from object_space import ObjectSpace 
from inertial_space import InertialSpace


class Transform( EventDispatcher ):


    def __init__( self ):
        super( Transform, self ).__init__()

        self._orientation = quaternion.identity()        
        self._translation = numpy.zeros( 3, dtype = numpy.float )
        self._scale = numpy.ones( 3, dtype = numpy.float )

    @property
    def object( self ):
        return ObjectSpace( self )

    @property
    def inertial( self ):
        return InertialSpace( self )
    
    @property
    def scale( self ):
        return self._scale

    @scale.setter
    def scale( self, scale ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._scale[:] = scale

        # notify others of our change
        self.dispatch_event(
            'on_transform_changed'
            )

    @property
    def orientation( self ):
        return self._orientation

    @orientation.setter
    def orientation( self, orientation ):
        """
        Stores the node's object orientation
        """
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._orientation[:] = orientation

        # notify others of our change
        self.dispatch_event(
            'on_transform_changed'
            )

    @property
    def translation( self ):
        """
        Returns the current inertial translation.
        """
        return self._translation
    
    @translation.setter
    def translation( self, vector ):
        """
        Sets the inertial translation of the node.
        """
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._translation[:] = vector

        # notify others of our change
        self.dispatch_event(
            'on_transform_changed'
            )

    @property
    def matrix( self ):
        """
        Returns a matrix representing the node's
        object translation, orientation and
        scale.
        """
        # matrix transformations must be done in order
        # scaling
        # rotation
        # translation

        # apply our scale
        matrix = matrix44.create_from_scale( self.scale )

        # apply our quaternion
        matrix44.multiply(
            matrix,
            matrix44.create_from_quaternion(
                self.orientation
                ),
            out = matrix
            )

        # apply our translation
        # we MUST do this after the orientation
        matrix44.multiply(
            matrix,
            matrix44.create_from_translation(
                self.translation,
                ),
            out = matrix
            )

        return matrix

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_transform_changed():
            '''The transform values were changed.

            :event:
            '''

Transform.register_event_type( 'on_transform_changed' )

