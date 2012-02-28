# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:35:44 2011

@author: adam

TODO: change drawing to use these python methods
http://www.pyglet.org/doc/programming_guide/drawing_primitives.html
"""

from pyglet.gl import *

import MD2


class MD2_Mesh( object ):
    
    def __init__( self, filename ):
        super( MD2_Mesh, self ).__init__()
        
        self.filename = filename
        self._frame = 0
        self.displayLists = []
    
    def load( self ):
        md2 = MD2.load( self.filename )
        
        # clear the existing display lists
        self.displayLists = []
        
        # iterate through the frames
        for frame in md2.frames:
            dl = glGenLists( 1 );
            glNewList( dl, GL_COMPILE )
            
            # use the vertices and normals from each frame
            # but draw them using the gl primitives
            for command in md2.gl_primitives:
                # begin the list
                if command.type > 0:
                    glBegin( GL_TRIANGLE_STRIP )
                else:
                    glBegin( GL_TRIANGLE_FAN )
                
                for index, indice in enumerate( command.indices ):
                    glTexCoord2f(
                        command.tcs[ (index, 0) ],
                        command.tcs[ (index, 1) ]
                        )
                    
                    glNormal3f(
                        frame.normals[ (indice, 0) ],
                        frame.normals[ (indice, 1) ],
                        frame.normals[ (indice, 2) ]
                        )
                    
                    glVertex3f(
                        frame.vertices[ (indice, 0) ],
                        frame.vertices[ (indice, 1) ],
                        frame.vertices[ (indice, 2) ]
                        )
                glEnd()
            
            glEndList()
            
            # add the display list
            self.displayLists.append( dl )
    
    def render( self ):
        glCallList( self.displayLists[ self._frame ] )
    
    @property
    def frames( self ):
        return len( self.displayLists )
    
    def _getFrame( self ):
        return self._frame
    
    def _setFrame( self, frame ):
        if frame > len( self.displayLists ):
            raise ValueError(
                'Invalid frame "%i" specified for mesh "%s"' % (
                    frame,
                    self.filename
                    )
                )
        
        self._frame = frame
    
    frame = property( _getFrame, _setFrame )
    
