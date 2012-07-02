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


class InertialSpace( object ):
    """Provides transform methods for manipulating objects within
    inertial space co-ordinates.

    Inertial space is defined as using the traslation of the object
    but the rotation remains relative to the parent.

    .. image:: _static/transform_inertial_space.png
    """

    def __init__( self, transform ):
        """Constructs an InertialSpace object that interacts with
        the specified transform object.

        Args:
            transform: The transform to control.
        """
        super( InertialSpace, self ).__init__()

        self.transform = transform

    def rotate_quaternion( self, quat ):
        raise NotImplementedError

    def rotate_x( self, radians ):
        raise NotImplementedError

    def rotate_y( self, radians ):
        raise NotImplementedError

    def rotate_z( self, radians ):
        raise NotImplementedError

    @property
    def translation( self ):
        """Returns the current inertial translation.
        """
        return self.transform._translation
    
    @translation.setter
    def translation( self, translation ):
        """Sets the inertial translation of the node.
        """
        # check for the translation not changing
        if numpy.array_equal(
            translation,
            self.transform._translation
            ):
            # don't bother to update anything
            return
        
        self.transform.translation = translation

    @property
    def x( self ):
        return numpy.array(
            [ 1.0, 0.0, 0.0 ],
            dtype = numpy.float
            )

    @property
    def y( self ):
        return numpy.array(
            [ 0.0, 1.0, 0.0 ],
            dtype = numpy.float
            )

    @property
    def z( self ):
        return numpy.array(
            [ 0.0, 0.0, 1.0 ],
            dtype = numpy.float
            )

    def translate( self, vector ):
        """Translates the node along it's inertial axis.

        The inertial axis of the object does not include
        it's local orientation.
        """
        if numpy.array_equal( vector, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return

        # apply the translation
        self.transform.translation += vector

