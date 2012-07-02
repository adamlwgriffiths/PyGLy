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


class ObjectSpace( object ):
    """Provides transform methods for manipulating objects within
    object space co-ordinates.

    Object space is defined as being relative to the object itself.
    The translation and orientation of the X,Y,Z axis remain fixed
    to the object as it moves.

    .. image:: _static/transform_object_space.png
    """

    def __init__( self, transform ):
        """Constructs an ObjectSpace object that interacts with
        the specified transform object.

        Args:
            transform: The transform to control.
        """
        super( ObjectSpace, self ).__init__()

        self.transform = transform

    def rotate_quaternion( self, quat ):
        """Rotates the transform by the specified orientation.
        """
        # check for the orientation not changing
        if numpy.array_equal(
            quat,
            [ 1.0, 0.0, 0.0, 0.0 ]
            ):
            # don't bother to update anything
            return
        
        # order of operations matters here
        # our orientation must be the second parameter
        self.transform.orientation = quaternion.cross(
            quat,
            self.transform._orientation
            )
    
    def rotate_x( self, radians ):
        """Pitch the transform about it's X axis.

        .. note::
            Amount > 0 == pitch down
            Amount < 0 == pitch up
        """
        if radians == 0.0:
            return

        quat = quaternion.set_to_rotation_about_x( radians )
        self.rotate_quaternion( quat )

    def rotate_y( self, radians ):
        """Yaw the transform about it's Y axis.

        .. note::
            Amount > 0 == yaw right.
            Amount < 0 == yaw left.
        """
        if radians == 0.0:
            return

        quat = quaternion.set_to_rotation_about_y( radians )
        self.rotate_quaternion( quat )
    
    def rotate_z( self, radians ):
        """Roll the transform about it's Z axis.

        .. note::
            Amount > 0 == roll left.
            Amount < 0 == roll right.
        """
        if radians == 0.0:
            return

        quat = quaternion.set_to_rotation_about_z( radians )
        self.rotate_quaternion( quat )

    @property
    def translation( self ):
        raise NotImplementedError
    
    @translation.setter
    def translation( self, translation ):
        raise NotImplementedError

    @property
    def x( self ):
        """Returns the object's local X axis.

        This is the X axis rotated by the objects
        orientation.

        .. note::
            This is NOT the world orientation.
            To get inertial X axis, simply use [1.0, 0.0, 0.0].
        """
        # convert our quaternion to a matrix
        matrix = matrix33.create_from_quaternion(
            self.transform.orientation
            )
        # apply the matrix to an X vector
        return matrix33.apply_to_vector(
            [1.0, 0.0, 0.0],
            matrix
            )

    @property
    def y( self ):
        """Returns the object's local Y axis.

        This is the Y axis rotated by the objects orientation.

        .. note::
            This is NOT the world orientation.
            To get inertial Y axis, simply use [0.0, 1.0, 0.0].
        """
        # convert our quaternion to a matrix
        matrix = matrix33.create_from_quaternion(
            self.transform.orientation
            )
        # apply the matrix to a Y vector
        return matrix33.apply_to_vector(
            [0.0, 1.0, 0.0],
            matrix
            )

    @property
    def z( self ):
        """Returns the object's local Z axis.

        This is the Z axis rotated by the objects
        orientation.
        
        .. note::
            This is NOT the world orientation.
            To get inertial Z axis, simply use [0.0, 0.0, 1.0].
        """
        # convert our quaternion to a matrix
        matrix = matrix33.create_from_quaternion(
            self.transform.orientation
            )
        # apply the matrix to a Y vector
        return matrix33.apply_to_vector(
            [0.0, 0.0, 1.0],
            matrix
            )

    def translate( self, vector ):
        """Translates the transform locally.

        The vector will have the node's current orientation
        applied to it and then be added to the translation.
        """
        if numpy.array_equal( vector, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return

        # multiply the vector by our local orientation
        # convert our quaternion to a matrix
        matrix = matrix33.create_from_quaternion(
            self.transform._orientation
            )
        # apply the matrix to an X vector
        self.transform.translation += matrix33.apply_to_vector(
            vector,
            matrix
            )

