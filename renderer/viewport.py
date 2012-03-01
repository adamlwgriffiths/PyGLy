'''
Created on 20/06/2011

@author: adam
'''

import weakref

import numpy
from pyglet.gl import *


class Viewport( object ):
    
    
    def __init__( self, width, height ):
        super( Viewport, self ).__init__()
        
        self.camera = None
        self.dimensions = numpy.array(
            [ width, height ],
            dtype = int
            )
        
        # setup our viewport
        self.update_viewport( self.width, self.height )
    
    @property
    def width( self ):
        return self.dimensions[ 0 ]
    
    @property
    def height( self ):
        return self.dimensions[ 1 ]
    
    def update_viewport( self, width, height ):
        self.dimensions[ 0 ] = width
        self.dimensions[ 1 ] = height
    
    def set_camera( self, camera ):
        self.camera = weakref.ref( camera )
    
    def set_active( self ):
        # update our viewport size
        glViewport( 0, 0, self.width, self.height )
    
    def setup_for_3d( self ):
        # z-buffer is disabled by default
        glEnable( GL_DEPTH_TEST )
        
        # the camera is a weak pointer
        # so we need to get a reference to it
        camera = None
        if self.camera != None:
            camera = self.camera()
        
        # setup our projection matrix
        if camera != None:
            glMatrixMode( GL_PROJECTION )
            glLoadIdentity()
            camera.apply_projection_matrix( self.width, self.height )
        
        # setup our model view matrix
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        
        if camera != None:
            # apply the camera's model view
            camera.apply_model_view()
    
    def setup_for_2d( self ):
        # disable z-buffer for 2d rendering
        glDisable( GL_DEPTH_TEST )
        
        # reset the projection matrix
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        
        # set the ortho matrix to be from
        # 0 -> width and 0 -> height
        # with near clip of -1 and far clip
        # of +1
        # http://stackoverflow.com/questions/4269079/mixing-2d-and-3d-in-opengl-using-pyglet
        glOrtho( 0, self.width, 0, self.height, -1.0, 1.0 )
        
        # reset the model view
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
    
