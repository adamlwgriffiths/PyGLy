'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
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
    """Provides translation and orientation information and
    methods for manipulating them.

    .. seealso::
        Class :py:class:`pygly.inertial_space.InertialSpace`
        Documentation of the
        :py:class:`pygly.inertial_space.InertialSpace`
        class.

        Class :py:class:`pygly.object_space.ObjectSpace`
        Documentation of the
        :py:class:`pygly.object_space.ObjectSpace`
        class.
    """


    def __init__( self ):
        """Constructs a transform object.
        """
        super( Transform, self ).__init__()

        self._orientation = quaternion.identity()        
        self._translation = numpy.zeros( 3, dtype = numpy.float )
        self._scale = numpy.ones( 3, dtype = numpy.float )
        self._matrix = None

    @property
    def object( self ):
        """Returns an ObjectSpace object for manipulating
        the transform in object space co-ordinates.

        .. seealso::
            Class :py:class:`pygly.object_space.ObjectSpace`
            Documentation of the
            :py:class:`pygly.object_space.ObjectSpace`
            class.
        """
        return ObjectSpace( self )

    @property
    def inertial( self ):
        """Returns an InertialSpace object for manipulating
        the transform in inertial space co-ordinates.

        .. seealso::
            Class :py:class:`pygly.inertial_space.InertialSpace`
            Documentation of the
            :py:class:`pygly.inertial_space.InertialSpace`
            class.
        """
        return InertialSpace( self )
    
    @property
    def scale( self ):
        """The scale of the transform.

        .. note:: Changing this value will dispatch an
        'on_transform_changed' event.

        .. note:: The is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        return self._scale

    @scale.setter
    def scale( self, scale ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._scale[:] = scale

        # mark our matrix as dirty
        self._matrix = None

        # notify others of our change
        self.dispatch_event(
            'on_transform_changed'
            )

    @property
    def orientation( self ):
        """The orientation of the transform.

        Changing this value will dispatch an
        'on_transform_changed' event.

        The is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        return self._orientation

    @orientation.setter
    def orientation( self, orientation ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._orientation[:] = orientation

        # mark our matrix as dirty
        self._matrix = None

        # notify others of our change
        self.dispatch_event(
            'on_transform_changed'
            )

    @property
    def translation( self ):
        """The translation of the transform.

        This is in inertial space.

        Changing this value will dispatch an
        'on_transform_changed' event.

        The is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        return self._translation
    
    @translation.setter
    def translation( self, vector ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        self._translation[:] = vector

        # mark our matrix as dirty
        self._matrix = None

        # notify others of our change
        self.dispatch_event(
            'on_transform_changed'
            )

    @property
    def matrix( self ):
        """A matrix representing the transform's translation,
        orientation and scale.

        The is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        if self._matrix == None:
            # matrix transformations must be done in order
            # scaling
            # rotation
            # translation

            # apply our scale
            self._matrix = matrix44.create_from_scale( self.scale )

            # apply our quaternion
            matrix44.multiply(
                self._matrix,
                matrix44.create_from_quaternion(
                    self.orientation
                    ),
                out = self._matrix
                )

            # apply our translation
            # we MUST do this after the orientation
            matrix44.multiply(
                self._matrix,
                matrix44.create_from_translation(
                    self.translation,
                    ),
                out = self._matrix
                )

        return self._matrix

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_transform_changed():
            '''The transform values were changed.

            :event:
            '''

Transform.register_event_type( 'on_transform_changed' )

