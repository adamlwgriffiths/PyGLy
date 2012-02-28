# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 20:20:11 2011

@author: adam
"""

import math

from Pyrr import Quaternion
from Pyrr import Matrix33


class FPS_Camera( object ):
    piOver2 = math.pi / 2.0
    
    def __init__( self ):
        super( FPS_Camera, self ).__init__()
        
        self.camera = None
        self.pitch = 0.0
        self.yaw = 0.0
    
    def setOrientation( self, pitch = None, yaw = None ):
        if pitch != None:
            self.pitch = pitch
        if yaw != None:
            self.yaw = yaw
        
        self.update()
    
    def orient( self, pitch = None, yaw = None ):
        if pitch != None:
            self.pitch += pitch
        if yaw != None:
            self.yaw += yaw
        
        self.update()
    
    def update( self ):
        # limit our pitch to +- 1/2 pi
        if self.pitch > self.piOver2:
            self.pitch = self.piOver2
        if self.pitch < -self.piOver2:
            self.pitch = -self.piOver2
        
        pitchQuat = Quaternion.setToRotationAboutX( self.pitch )
        yawQuat = Quaternion.setToRotationAboutY( self.yaw )
        
        quat = Quaternion.crossProduct( pitchQuat, yawQuat )
        Quaternion.normalise( quat )
        self.camera.orientation = quat
    
    def translateObjectForward( self, amount ):
        self.camera.translateForward( amount )
    
    def translateObjectBackward( self, amount ):
        self.camera.translateBackward( amount )
    
    def translateInertialForward( self, amount ):
        vec = [ 0.0, 0.0, -1.0 ]
        rotationQuat = Quaternion.setToRotationAboutY( self.yaw )
        
        matrix = Matrix33.fromInertialToObjectQuaternion( rotationQuat )
        forwardVec = Matrix33.inertialToObject( vec, matrix )
        forwardVec *= amount
        
        self.camera.translate( forwardVec )
    
    def translateInertialBackward( self, amount ):
        vec = [ 0.0, 0.0, 1.0 ]
        rotationQuat = Quaternion.setToRotationAboutY( self.yaw )
        
        matrix = Matrix33.fromInertialToObjectQuaternion( rotationQuat )
        backwardVec = Matrix33.inertialToObject( vec, matrix )
        backwardVec *= amount
        
        self.camera.translate( backwardVec )
    
    def translateInertialUp( self, amount ):
        self.camera.translate( [ 0.0, amount, 0.0 ] )
    
    def translateInertialDown( self, amount ):
        self.camera.translate( [ 0.0, -amount, 0.0 ] )
    
    def translateObjectUp( self, amount ):
        self.camera.translateUp( amount )
    
    def translateObjectDown( self, amount ):
        self.camera.translateDown( amount )
    
    def translateLeft( self, amount ):
        self.camera.translateLeft( amount )
    
    def translateRight( self, amount ):
        self.camera.translateRight( amount )
    
