# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 15:03:23 2011

@author: adam
"""


class Mesh( object ):
    
    def __init__( self ):
        self.vertices = []
        self.normals = []
        self.textureCoords = []
        
        self.points = []
        self.triangles = []
        self.quads = []
        self.trifans = []
        self.tristrips = []
        self.quadstrips = []
        
        self.material = None
    
    def load( self ):
        pass
    
    def setTime( self, time ):
        pass
    
    def render( self ):
        pass
    
