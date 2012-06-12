# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:20:52 2011

@author: adam
"""

import math

from pyrr import quaternion


class SixDOF_Controller( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self, transform = None ):
        super( SixDOF_Controller, self ).__init__()
        
        self.transform = transform
    
    def orient( self, pitch = None, yaw = None, roll = None ):
        """
        Over-ride the current orientation.
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
        """
        Translates the object along the -Z object axis.
        """
        self.translate_backward( -amount )
    
    def translate_backward( self, amount ):
        """
        Translates the object along the +Z object axis.
        """
        self.transform.object.translate(
            [ 0.0, 0.0, amount ]
            )
    
    def translate_up( self, amount ):
        """
        Translates the object along the +Y object axis.
        """
        self.transform.object.translate(
            [ 0.0, amount, 0.0 ]
            )
    
    def translate_down( self, amount ):
        """
        Translates the object along the -Y object axis.
        """
        self.translate_up( -amount )
    
    def translate_left( self, amount ):
        """
        Translates the object along the -X object axis.
        """
        self.translate_right( -amount )
    
    def translate_right( self, amount ):
        """
        Translates the object along the +X object axis.
        """
        self.transform.object.translate(
            [ amount, 0.0, 0.0 ]
            )
    
