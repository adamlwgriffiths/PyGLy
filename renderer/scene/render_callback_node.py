# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:01:19 2011

@author: adam
"""

from pyglet.gl import *

from RenderNode import RenderNode


class RenderCallbackNode( RenderNode ):
    
    
    def __init__( self, name, initialiseCallback, renderCallback ):
        super( RenderCallbackNode, self ).__init__( name )
        
        if renderCallback == None:
            raise ValueError( "RenderNode renderCallback cannot be None" )
        
        self.initialiseCallback = initialiseCallback
        self.renderCallback = renderCallback
        
        # initialise the mesh now
        self.initialiseCallback()
    
    def onContextLost( self ):
        # re-create any data for the mesh
        self.initialiseCallback()
        
        # let our children know
        for child in self.children:
            child.onContextLost()
    
    def render( self ):
        # apply our transforms
        glPushMatrix()
        
        self.applyTranslations()
        
        if self.renderDebugCube == True:
            DebugCube.renderDebugCube()
        
        self.renderCallback()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()
    


