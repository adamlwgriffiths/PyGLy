"""Controls a transform to provide a 'First Person Shooter-like'
interface.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

import math

from pyrr import quaternion
from pyrr import matrix33


class FPS_Controller( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self, transform = None ):
        """Creates an FPS_Controller that controls the
        specified transform object.

        Args:
            transform: The transform to control.
            Having this as an option allows the node
            to be controlled locally or via world coordinates.
        """
        super( FPS_Controller, self ).__init__()
        
        #: The transform being controlled.
        self.transform = transform
        #: The current pitch.
        self.pitch = 0.0
        #: The current yaw.
        self.yaw = 0.0
    
    def set_orientation( self, pitch = None, yaw = None ):
        """Over-ride the current orientation.

        Automatically calls _update at the end.
        TODO: add roll
        """
        if pitch != None:
            self.pitch = pitch
        if yaw != None:
            self.yaw = yaw
        
        self._update()
    
    def orient( self, pitch = None, yaw = None ):
        """Add to the current orientation.

        Automatically calls _update at the end.
        TODO: add roll
        """
        if pitch != None:
            self.pitch += pitch
        if yaw != None:
            self.yaw += yaw
        
        self._update()
    
    def _update( self ):
        """Updates the orientation of the object.

        This should be called once all of the yaw / pitch
        modifications are applied.
        """
        # limit our pitch to +- 1/2 pi
        if self.pitch > self.piOver2:
            self.pitch = self.piOver2
        if self.pitch < -self.piOver2:
            self.pitch = -self.piOver2
        
        pitchQuat = quaternion.set_to_rotation_about_x( self.pitch )
        yawQuat = quaternion.set_to_rotation_about_y( self.yaw )
        
        quat = quaternion.cross( pitchQuat, yawQuat )
        quaternion.normalise( quat )
        self.transform.orientation = quat

    def translate_up( self, amount ):
        """Translates the object up the Y inertial axis.
        """
        self.transform.inertial.translate(
            [ 0.0, amount, 0.0 ]
            )

    def translate_down( self, amount ):
        """Translates the object down the Y inertial axis.
        """
        self.translate_up( -amount )

    def translate_forward( self, amount ):
        """Translates the object forward along the inertial X,Z
        plane.
        """
        quat = quaternion.set_to_rotation_about_y( self.yaw )

        matrix = matrix33.create_from_quaternion( quat )
        vec = matrix33.apply_to_vector(
            [0.0, 0.0,-1.0],
            matrix
            )
        vec *= amount
        self.transform.inertial.translate( vec )

    def translate_backward( self, amount ):
        """Translates the object backward along the inertial X,Z
        plane.
        """
        quat = quaternion.set_to_rotation_about_y( self.yaw )

        matrix = matrix33.create_from_quaternion( quat )
        vec = matrix33.apply_to_vector(
            [0.0, 0.0, 1.0],
            matrix
            )
        vec *= amount
        self.transform.inertial.translate( vec )
    
    def translate_left( self, amount ):
        """Translates the object left along the inertial X,Z
        plane.
        """
        self.translate_right( -amount )
    
    def translate_right( self, amount ):
        """Translates the object right along the inertial X,Z
        plane.
        """
        self.transform.object.translate(
            [ amount, 0.0, 0.0 ]
            )
    

