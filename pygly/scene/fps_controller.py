# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 20:20:11 2011

@author: adam
"""

import math

import maths.quaternion
import maths.matrix33


class FPS_Controller( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self ):
        super( FPS_Controller, self ).__init__()
        
        self.scene_node = None
        self.pitch = 0.0
        self.yaw = 0.0
    
    def set_orientation( self, pitch = None, yaw = None ):
        """
        Over-ride the current orientation.
        Automatically calls update at the end.
        TODO: add roll
        """
        if pitch != None:
            self.pitch = pitch
        if yaw != None:
            self.yaw = yaw
        
        self._update()
    
    def orient( self, pitch = None, yaw = None ):
        """
        Add to the current orientation.
        Automatically calls update at the end.
        TODO: add roll
        """
        if pitch != None:
            self.pitch += pitch
        if yaw != None:
            self.yaw += yaw
        
        self._update()
    
    def _update( self ):
        """
        Updates the orientation of the object.
        This should be called once all of the yaw / pitch
        modifications are applied.
        """
        # limit our pitch to +- 1/2 pi
        if self.pitch > self.piOver2:
            self.pitch = self.piOver2
        if self.pitch < -self.piOver2:
            self.pitch = -self.piOver2
        
        pitchQuat = maths.quaternion.set_to_rotation_about_x( self.pitch )
        yawQuat = maths.quaternion.set_to_rotation_about_y( self.yaw )
        
        quat = maths.quaternion.cross_product( pitchQuat, yawQuat )
        maths.quaternion.normalise( quat )
        self.scene_node.orientation = quat

    def translate_up( self, amount ):
        """
        Translates the object up the Y inertial axis.
        """
        self.scene_node.translate_inertial_y( amount )

    def translate_down( self, amount ):
        """
        Translates the object down the Y inertial axis.
        """
        self.scene_node.translate_inertial_y( -amount )

    def translate_forward( self, amount ):
        """
        Translates the object forward along the inertial X,Z
        plane.
        """
        quat = maths.quaternion.set_to_rotation_about_y( self.yaw )

        matrix = maths.matrix33.from_inertial_to_object_quaternion( quat )
        vec = maths.matrix33.inertial_to_object(
            [0.0, 0.0,-1.0],
            matrix
            )
        vec *= amount
        self.scene_node.translate_inertial( vec )

    def translate_backward( self, amount ):
        """
        Translates the object backward along the inertial X,Z
        plane.
        """
        quat = maths.quaternion.set_to_rotation_about_y( self.yaw )

        matrix = maths.matrix33.from_inertial_to_object_quaternion( quat )
        vec = maths.matrix33.inertial_to_object(
            [0.0, 0.0, 1.0],
            matrix
            )
        vec *= amount
        self.scene_node.translate_inertial( vec )
    
    def translate_left( self, amount ):
        """
        Translates the object left along the inertial X,Z
        plane.
        """
        self.scene_node.translate_object_x( -amount )
    
    def translate_right( self, amount ):
        """
        Translates the object right along the inertial X,Z
        plane.
        """
        self.scene_node.translate_object_x( amount )
    
