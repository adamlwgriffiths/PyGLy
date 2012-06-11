'''
Created on 25/03/2012

@author: adam
'''

from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.text import Label


display_list = None
label_x = None
label_y = None
label_z = None

def initialise():
    global display_list
    display_list = glGenLists( 1 )
    glNewList( display_list, GL_COMPILE )

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

    glEndList()

    # create some labels
    global label_x
    global label_y
    global label_z

    font = 'Times New Roman'
    font_size = 18
    dpi = 200.0

    label_x = Label(
        'X',
        font_name = font,
        font_size = font_size,
        dpi = dpi,
        anchor_x = 'center',
        anchor_y = 'center'
        )
    label_y = Label(
        'Y',
        font_name = font,
        font_size = font_size,
        dpi = dpi,
        anchor_x = 'center',
        anchor_y = 'center'
        )
    label_z = Label(
        'Z',
        font_name = font,
        font_size = font_size,
        dpi = dpi,
        anchor_x = 'center',
        anchor_y = 'center'
        )

def render():
    global display_list
    global label_x
    global label_y
    global label_z

    if display_list == None:
        initialise()

    # we're going to mess around with GL state
    # so push the existing values on the stack
    glPushAttrib( GL_ALL_ATTRIB_BITS )
    glPushMatrix()

    # change the line width
    glLineWidth( 3.0 )

    # render the axis
    scale = 5.0
    inv_scale = 1.0 / scale
    glScalef( scale, scale, scale )
    glCallList( display_list )
    glScalef( inv_scale, inv_scale, inv_scale )

    # enable alpha blending
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE )
    glBlendEquation( GL_FUNC_ADD )

    # disable back face culling
    glDisable( GL_CULL_FACE )

    # disable depth buffer
    # transparent objects still write to depth buffer
    # so normally you would render solid geometry
    # then back to front for transparent
    # we don't want the transparent objects causing
    # other objects to not render beheind them
    glDepthMask( GL_FALSE )

    translation = 5.0
    scale = 0.1
    inv_scale = 1.0 / scale

    # draw X label
    glTranslatef( translation, 0.0, 0.0 )
    glScalef( scale, scale, scale )
    label_x.draw()
    glScalef( inv_scale, inv_scale, inv_scale )

    # draw Y label
    glTranslatef(-translation, translation, 0.0 )
    glScalef( scale, scale, scale )
    label_y.draw()
    glScalef( inv_scale, inv_scale, inv_scale )

    # draw Z label
    glTranslatef( 0.0,-translation, translation )
    # rotate down z axis
    glRotatef( 90.0, 0.0, 1.0, 0.0 )
    glScalef( scale, scale, scale )
    label_z.draw()
    glScalef( inv_scale, inv_scale, inv_scale )

    # reset our gl state
    glPopMatrix()
    glPopAttrib()

