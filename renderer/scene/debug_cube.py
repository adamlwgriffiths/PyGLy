'''
Created on 29/06/2011

@author: adam
'''

from pyglet.gl import *


def render_debug_cube():
    # render a cube at our scene node for debugging
    glBegin( GL_QUADS )
    # green
    glColor3f( 0.0, 1.0, 0.0 )
    glVertex3f( 1.0, 1.0,-1.0 )
    glVertex3f(-1.0, 1.0,-1.0 )
    glVertex3f(-1.0, 1.0, 1.0 )
    glVertex3f( 1.0, 1.0, 1.0 )
    
    # orange
    glColor3f( 1.0, 0.5, 0.0 )
    glVertex3f( 1.0,-1.0, 1.0 )
    glVertex3f(-1.0,-1.0, 1.0 )
    glVertex3f(-1.0,-1.0,-1.0 )
    glVertex3f( 1.0,-1.0,-1.0 )
    
    # red
    glColor3f( 1.0, 0.0, 0.0 )
    glVertex3f( 1.0, 1.0, 1.0 )
    glVertex3f(-1.0, 1.0, 1.0 )
    glVertex3f(-1.0,-1.0, 1.0 )
    glVertex3f( 1.0,-1.0, 1.0 )
    
    # yellow
    glColor3f( 1.0, 1.0, 0.0 )
    glVertex3f( 1.0,-1.0,-1.0 )
    glVertex3f(-1.0,-1.0,-1.0 )
    glVertex3f(-1.0, 1.0,-1.0 )
    glVertex3f( 1.0, 1.0,-1.0 )
    
    # blue
    glColor3f( 0.0, 0.0, 1.0 )
    glVertex3f(-1.0, 1.0, 1.0 )
    glVertex3f(-1.0, 1.0,-1.0 )
    glVertex3f(-1.0,-1.0,-1.0 )
    glVertex3f(-1.0,-1.0, 1.0 )
    
    # violet
    glColor3f( 1.0, 0.0, 1.0 )
    glVertex3f( 1.0, 1.0,-1.0 )
    glVertex3f( 1.0, 1.0, 1.0 )
    glVertex3f( 1.0,-1.0, 1.0 )
    glVertex3f( 1.0,-1.0,-1.0 )
    
    glEnd()

