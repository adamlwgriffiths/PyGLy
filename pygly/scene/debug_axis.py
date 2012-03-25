'''
Created on 25/03/2012

@author: adam
'''

from pyglet.gl import *
from pyglet.graphics import Batch


display_list = None

def initialise():
    global display_list
    display_list = glGenLists( 1 )
    glNewList( display_list, GL_COMPILE )

    # TODO: store existing line width value
    glLineWidth( 1.0 )

    # draw the axis
    glBegin( GL_LINES )

    # X axis
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 1.0, 0.0, 0.0 )

    # Y axis
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 0.0, 1.0, 0.0 )

    # Z axis
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 0.0, 0.0, 1.0 )

    glEnd()

    # draw the axis labels

    # pyglet text labels are too blurry and we
    # can't put them in display lists
    # so we'll do some leet hax and draw our letters
    # X label = \ + /
    glTranslatef( 2.0, 0.0, 0.0 )
    glBegin( GL_LINES )
    # \
    glVertex3f(-1.0, 1.0, 0.0 )
    glVertex3f( 1.0,-1.0, 0.0 )
    # /
    glVertex3f(-1.0,-1.0, 0.0 )
    glVertex3f( 1.0, 1.0, 0.0 )
    glEnd()
    glTranslatef(-2.0, 0.0, 0.0 )

    # Y label = V + |
    glTranslatef( 0.0, 2.0, 0.0 )
    glBegin( GL_LINE_STRIP )
    # V
    glVertex3f(-1.0, 1.0, 0.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 1.0, 1.0, 0.0 )
    glEnd()
    # |
    glBegin( GL_LINES )
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 0.0,-1.0, 0.0 )
    glEnd()
    glTranslatef( 0.0,-2.0, 0.0 )

    # Z label = - + / + -
    # we shall draw the z label along the Y/Z axis, not X/Y
    # -
    glTranslatef( 0.0, 0.0, 2.0 )
    glBegin( GL_LINE_STRIP )
    glVertex3f( 0.0, 1.0,-1.0 )
    glVertex3f( 0.0, 1.0, 1.0 )
    # /
    glVertex3f( 0.0,-1.0,-1.0 )
    # -
    glVertex3f( 0.0,-1.0, 1.0 )
    glEnd()
    glTranslatef( 0.0, 0.0,-2.0 )

    glEndList()

def render():
    global display_list

    if display_list == None:
        initialise()

    # render the axis
    glCallList( display_list )

