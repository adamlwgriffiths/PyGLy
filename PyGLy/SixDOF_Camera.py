# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:20:52 2011

@author: adam
"""

import math

from Pyrr import Quaternion
from Pyrr import Matrix33


class SixDOF_Camera( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self ):
        super( SixDOF_Camera, self ).__init__()
        
        self.camera = None
    
    def orient( self, pitch = None, yaw = None, roll = None ):
        if yaw != None:
            quat = Quaternion.setToRotationAboutY( yaw )
            Quaternion.crossProduct(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # mark the camera as dirty because the
            # out= above doesn't trigger the property set method
            self.camera._setDirty()
        if pitch != None:
            quat = Quaternion.setToRotationAboutX( pitch )
            Quaternion.crossProduct(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # mark the camera as dirty because the
            # out= above doesn't trigger the property set method
            self.camera._setDirty()
        if roll != None:
            quat = Quaternion.setToRotationAboutZ( roll )
            Quaternion.crossProduct(
                quat,
                self.camera.orientation,
                out = self.camera.orientation
                )
            # mark the camera as dirty because the
            # out= above doesn't trigger the property set method
            self.camera._setDirty()
    
    def translateForward( self, amount ):
        self.camera.translateForward( amount )
    
    def translateBackward( self, amount ):
        self.camera.translateBackward( amount )
    
    def translateUp( self, amount ):
        self.camera.translateUp( amount )
    
    def translateDown( self, amount ):
        self.camera.translateDown( amount )
    
    def translateLeft( self, amount ):
        self.camera.translateLeft( amount )
    
    def translateRight( self, amount ):
        self.camera.translateRight( amount )
    
