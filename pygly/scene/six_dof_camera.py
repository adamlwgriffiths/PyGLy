# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:20:52 2011

@author: adam
"""

import math

import maths.quaternion


class SixDOF_Camera( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self ):
        super( SixDOF_Camera, self ).__init__()
        
        self.camera = None
    
    def orient( self, pitch = None, yaw = None, roll = None ):
        """
        Over-ride the current orientation.
        """
        if yaw != None:
            quat = maths.quaternion.set_to_rotation_about_y( yaw )
            maths.quaternion.cross_product(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # we MUST manually set the node as dirty
            # when we update the quaternion in
            # place, the 'setter' function is not
            # called and the node's 'dirty' flag does
            # not get set
            self.camera._set_dirty()
        if pitch != None:
            quat = maths.quaternion.set_to_rotation_about_x( pitch )
            maths.quaternion.cross_product(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # we MUST manually set the node as dirty
            # when we update the quaternion in
            # place, the 'setter' function is not
            # called and the node's 'dirty' flag does
            # not get set
            self.camera._set_dirty()
        if roll != None:
            quat = maths.quaternion.set_to_rotation_about_z( roll )
            maths.quaternion.cross_product(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # we MUST manually set the node as dirty
            # when we update the quaternion in
            # place, the 'setter' function is not
            # called and the node's 'dirty' flag does
            # not get set
            self.camera._set_dirty()
    
    def translate_forward( self, amount ):
        """
        Translates the object forward
        based upon it's current orientation.
        """
        self.camera.translate_forward( amount )
    
    def translate_backward( self, amount ):
        """
        Translates the object backward
        based upon it's current orientation.
        """
        self.camera.translate_backward( amount )
    
    def translate_up( self, amount ):
        """
        Translates the object up
        based upon it's current orientation.
        """
        self.camera.translate_up( amount )
    
    def translate_down( self, amount ):
        """
        Translates the object down
        based upon it's current orientation.
        """
        self.camera.translate_down( amount )
    
    def translate_left( self, amount ):
        """
        Translates the object left
        based upon it's current orientation.
        """
        self.camera.translate_left( amount )
    
    def translate_right( self, amount ):
        """
        Translates the object right
        based upon it's current orientation.
        """
        self.camera.translate_right( amount )
    
