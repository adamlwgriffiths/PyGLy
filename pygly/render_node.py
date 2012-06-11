# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:01:19 2011

@author: adam
"""

from pyglet.gl import *

from scene_node import SceneNode


class RenderNode( SceneNode ):
    
    
    def __init__( self, name ):
        super( RenderNode, self ).__init__( name )
    
    def on_context_lost( self ):
        pass
    
    def render( self ):
        # store the existing matrix state
        glPushMatrix()

        # apply our transforms
        matrix = self.world_transform.matrix
        glMultMatrixf(
            (GLfloat * matrix.size)(*matrix.flat)
            )
        
        # render ourself
        self.render_mesh()

        # undo our transforms
        glPopMatrix()
        
    def render_mesh( self ):
        pass

