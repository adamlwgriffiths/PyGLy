# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:20:52 2011

@author: adam
"""

import math

import maths.quaternion


class SixDOF_Controller( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self ):
        super( SixDOF_Controller, self ).__init__()
        
        self.scene_node = None
    
    def orient( self, pitch = None, yaw = None, roll = None ):
        """
        Over-ride the current orientation.
        """
        if yaw != None:
            quat = maths.quaternion.set_to_rotation_about_y( yaw )
            maths.quaternion.cross_product(
                quat,
                self.scene_node.orientation,
                out = self.scene_node.orientation
                )
            # we MUST manually set the node as dirty
            # when we update the quaternion in
            # place, the 'setter' function is not
            # called and the node's 'dirty' flag does
            # not get set
            self.scene_node._set_dirty()
        if pitch != None:
            quat = maths.quaternion.set_to_rotation_about_x( pitch )
            maths.quaternion.cross_product(
                quat,
                self.scene_node.orientation,
                out = self.scene_node.orientation
                )
            # we MUST manually set the node as dirty
            # when we update the quaternion in
            # place, the 'setter' function is not
            # called and the node's 'dirty' flag does
            # not get set
            self.scene_node._set_dirty()
        if roll != None:
            quat = maths.quaternion.set_to_rotation_about_z( roll )
            maths.quaternion.cross_product(
                quat,
                self.scene_node.orientation,
                out = self.scene_node.orientation
                )
            # we MUST manually set the node as dirty
            # when we update the quaternion in
            # place, the 'setter' function is not
            # called and the node's 'dirty' flag does
            # not get set
            self.scene_node._set_dirty()
    
    def translate_forward( self, amount ):
        """
        Translates the object along the -Z object axis.
        """
        self.scene_node.translate_object_z( -amount )
    
    def translate_backward( self, amount ):
        """
        Translates the object along the +Z object axis.
        """
        self.scene_node.translate_object_z( amount )
    
    def translate_up( self, amount ):
        """
        Translates the object along the +Y object axis.
        """
        self.scene_node.translate_object_y( amount )
    
    def translate_down( self, amount ):
        """
        Translates the object along the -Y object axis.
        """
        self.scene_node.translate_object_y( -amount )
    
    def translate_left( self, amount ):
        """
        Translates the object along the -X object axis.
        """
        self.scene_node.translate_object_x( -amount )
    
    def translate_right( self, amount ):
        """
        Translates the object along the +X object axis.
        """
        self.scene_node.translate_object_x( amount )
    
