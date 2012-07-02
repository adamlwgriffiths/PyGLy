'''
Renders axis information for visualising 3D coordinates.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.text import Label


display_list = None
label_x = None
label_y = None
label_z = None

def initialise_axis():
    """Initialises the axis render objects.
    """
    global display_list

    display_list = glGenLists( 1 )
    glNewList( display_list, GL_COMPILE )

    # draw the axis
    glBegin( GL_LINES )

    # X axis
    glColor3f( 1.0, 0.0, 0.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 1.0, 0.0, 0.0 )
    # arrow
    glVertex3f( 0.7, 0.3, 0.0 )
    glVertex3f( 1.0, 0.0, 0.0 )
    glVertex3f( 0.7,-0.3, 0.0 )
    glVertex3f( 1.0, 0.0, 0.0 )

    # Y axis
    glColor3f( 0.0, 1.0, 0.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 0.0, 1.0, 0.0 )
    # arrow
    glVertex3f(-0.3, 0.7, 0.0 )
    glVertex3f( 0.0, 1.0, 0.0 )
    glVertex3f( 0.3, 0.7, 0.0 )
    glVertex3f( 0.0, 1.0, 0.0 )

    # Z axis
    glColor3f( 0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glVertex3f( 0.0, 0.0, 1.0 )
    # arrow
    glVertex3f( 0.0, -0.3, 0.7 )
    glVertex3f( 0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.3, 0.7 )
    glVertex3f( 0.0, 0.0, 1.0 )

    glEnd()

    glEndList()

def initialise_labels():
    """Initialises the label render objects.
    """
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

def initialise():
    """Initialises the axis and label objects.
    """
    initialise_axis()
    initialise_labels()

def render_axis():
    """Renders the axis arrows.
    """
    global display_list

    if display_list == None:
        initialise_axis()

    # we're going to mess around with GL state
    # so push the existing values on the stack
    glPushAttrib( GL_ALL_ATTRIB_BITS )
    glPushMatrix()

    # change the line width
    glLineWidth( 5.0 )

    # render the axis
    scale = 5.0
    inv_scale = 1.0 / scale

    glScalef( scale, scale, scale )
    glCallList( display_list )
    glScalef( inv_scale, inv_scale, inv_scale )

    # reset our gl state
    glPopMatrix()
    glPopAttrib()

def render_labels():
    """Renders the axis labels.
    """
    global label_x
    global label_y
    global label_z

    if \
        label_x == None or \
        label_y == None or \
        label_z == None:
        initialise_labels()

    # we're going to mess around with GL state
    # so push the existing values on the stack
    glPushAttrib( GL_ALL_ATTRIB_BITS )
    glPushMatrix()

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

    translation = 6.0
    scale = 0.05
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

def render():
    """Renders the axis arrows and labels.
    """
    render_axis()
    render_labels()


