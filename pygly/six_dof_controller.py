"""Controls a transform to provide a 6 degree of freedom
interface.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
"""

import math

from pyrr import quaternion


class SixDOF_Controller( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self, transform = None ):
        """Creates a SixDOF_Controller that controls the
        specified transform object.

        Args:
            transform: The transfom to control.
            Having this as an option allows the node
            to be controlled locally or via world coordinates.
        """
        super( SixDOF_Controller, self ).__init__()
        
        #: The transform being controlled.
        self.transform = transform
    
    def orient( self, pitch = None, yaw = None, roll = None ):
        """Over-ride the current orientation.
        """
        if yaw != None:
            quat = quaternion.set_to_rotation_about_y( yaw )
            self.transform.orientation = quaternion.cross(
                quat,
                self.transform.orientation
                )
        if pitch != None:
            quat = quaternion.set_to_rotation_about_x( pitch )
            self.transform.orientation = quaternion.cross(
                quat,
                self.transform.orientation
                )
        if roll != None:
            quat = quaternion.set_to_rotation_about_z( roll )
            self.transform.orientation = quaternion.cross(
                quat,
                self.transform.orientation
                )
    
    def translate_forward( self, amount ):
        """Translates the transform along the -Z object axis.
        """
        self.translate_backward( -amount )
    
    def translate_backward( self, amount ):
        """Translates the transform along the +Z object axis.
        """
        self.transform.object.translate(
            [ 0.0, 0.0, amount ]
            )
    
    def translate_up( self, amount ):
        """Translates the transform along the +Y object axis.
        """
        self.transform.object.translate(
            [ 0.0, amount, 0.0 ]
            )
    
    def translate_down( self, amount ):
        """Translates the transform along the -Y object axis.
        """
        self.translate_up( -amount )
    
    def translate_left( self, amount ):
        """Translates the transform along the -X object axis.
        """
        self.translate_right( -amount )
    
    def translate_right( self, amount ):
        """Translates the transform along the +X object axis.
        """
        self.transform.object.translate(
            [ amount, 0.0, 0.0 ]
            )
    
