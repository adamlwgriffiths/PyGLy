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
        if yaw != None:
            quat = maths.quaternion.set_to_rotation_about_y( yaw )
            maths.quaternion.cross_product(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # mark the camera as dirty because the
            # out= above doesn't trigger the property set method
            self.camera._setDirty()
        if pitch != None:
            quat = maths.quaternion.set_to_rotation_about_x( pitch )
            maths.quaternion.cross_product(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # mark the camera as dirty because the
            # out= above doesn't trigger the property set method
            self.camera._setDirty()
        if roll != None:
            quat = maths.quaternion.set_to_rotation_about_z( roll )
            maths.quaternion.cross_product(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # mark the camera as dirty because the
            # out= above doesn't trigger the property set method
            self.camera._setDirty()
    
    def translate_forward( self, amount ):
        self.camera.translate_forward( amount )
    
    def translate_backward( self, amount ):
        self.camera.translatebackward( amount )
    
    def translate_up( self, amount ):
        self.camera.translate_ip( amount )
    
    def translate_down( self, amount ):
        self.camera.translate_down( amount )
    
    def translate_left( self, amount ):
        self.camera.translate_left( amount )
    
    def translate_right( self, amount ):
        self.camera.translate_right( amount )
    
