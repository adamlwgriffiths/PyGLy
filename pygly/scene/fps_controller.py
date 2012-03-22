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
    
    def translate_object_forward( self, amount ):
        """
        Moves the object forward relative to
        it's own orientation.
        """
        self.scene_node.translate_forward( amount )
    
    def translate_object_backward( self, amount ):
        """
        Moves the object backward relative to
        it's own orientation.
        """
        self.scene_node.translateBackward( amount )
    
    def translate_inertial_forward( self, amount ):
        """
        Moves the object forward along the X,Z
        plane ignoring the objects orientation.
        """
        vec = [ 0.0, 0.0, -1.0 ]
        rotationQuat = maths.quaternion.set_to_rotation_about_y( self.yaw )
        
        matrix = maths.matrix33.from_inertial_to_object_quaternion( rotationQuat )
        forwardVec = maths.matrix33.inertial_to_object( vec, matrix )
        forwardVec *= amount
        
        self.scene_node.translate( forwardVec )
    
    def translate_inertial_backward( self, amount ):
        """
        Moves the object backward along the X,Z
        plane ignoring the objects orientation.
        """
        vec = [ 0.0, 0.0, 1.0 ]
        rotationQuat = maths.quaternion.set_to_rotation_about_y( self.yaw )
        
        matrix = maths.matrix33.from_inertial_to_object_quaternion( rotationQuat )
        backwardVec = maths.matrix33.inertial_to_object( vec, matrix )
        backwardVec *= amount
        
        self.scene_node.translate( backwardVec )
    
    def translate_inertial_up( self, amount ):
        """
        Moves the object up the Z axis
        ignoring the objects orientation.
        """
        self.scene_node.translate( [ 0.0, amount, 0.0 ] )
    
    def translate_inertial_down( self, amount ):
        """
        Moves the object down the Z axis
        ignoring the objects orientation.
        """
        self.scene_node.translate( [ 0.0, -amount, 0.0 ] )
    
    def translate_object_up( self, amount ):
        """
        Moves the object upward relative to
        it's own orientation.
        """
        self.scene_node.translate_up( amount )
    
    def translate_object_down( self, amount ):
        """
        Moves the object downward relative to
        it's own orientation.
        """
        self.scene_node.translate_down( amount )

    def translate_forward( self, amount ):
        """
        The same as translate_inertial_forward.
        Moves the object forward along the X,Z
        plane.
        """
        self.translate_inertial_forward( amount )

    def translate_backward( self, amount ):
        """
        The same as translate_inertial_backward.
        Moves the object backward along the X,Z
        plane.
        """
        self.translate_inertial_backward( amount )
    
    def translate_left( self, amount ):
        """
        In FPS, theres is no difference
        between intertial left, and object left.
        """
        self.scene_node.translate_left( amount )
    
    def translate_right( self, amount ):
        """
        In FPS, theres is no difference
        between intertial right, and object right.
        """
        self.scene_node.translate_right( amount )
    
