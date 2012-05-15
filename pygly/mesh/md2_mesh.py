# -*- coding: utf-8 -*-
"""
Created on 02/04/2012

@author: adam
"""

import os
import math
import struct
from collections import namedtuple

import numpy
from pyglet.gl import *

from md2 import MD2
from pyrr import vector


class MD2_Mesh( object ):
    
    def __init__( self, filename ):
        super( MD2_Mesh, self ).__init__()
        
        self.filename = filename
        self.frame = 0.0
        self.md2 = MD2()

    def load( self ):
        """
        Reads the MD2 data from the existing
        specified filename.
        """
        self.md2.load( self.filename )

    def render_frame( self, frame ):
        """
        Renders the specified frame using pyglet.graphics.draw.

        @param frame: the frame to draw. This can be an integer
        or a float.
        If a float is passed, the fractional value will be
        used for interpolation of the frames.
        Interpolation is done on the fly and can be slow.
        """
        # split the frame time into whole and fractional parts
        # the whole part is the current frame
        # the fractional part is the % through the frame
        delta, current_frame = math.modf( frame )
        current_frame = int(current_frame)

        # using the vertices for this frame, pull out the
        # vertices in order of our triangles
        # do the same for the normals
        vertices = self.md2.frames[ current_frame ].vertices
        normals = self.md2.frames[ current_frame ].normals

        # interpolate between this frame and the next
        # only do this is the time is not 0.0
        # and we're not at the end of the list
        if delta > 0.0:
            next_vertices = self.md2.frames[ current_frame + 1 ].vertices
            next_normals = self.md2.frames[ current_frame + 1 ].normals

            # scale the difference based on the time
            vertices = vector.interpolate( vertices, next_vertices, delta )
            normals = vector.interpolate( normals, next_normals, delta )

            # ensure our normals are vector length
            vector.normalise( normals )

        # pass to opengl
        pyglet.graphics.draw(
            vertices.size / 3,
            GL_TRIANGLES,
            ('v3f/static', vertices.flatten()),
            ('n3f/static', normals.flatten()),
            ('t2f/static', self.md2.tcs.flatten())
            )

    def render( self ):
        """
        Renders the currently set frame.
        """
        self.render_frame( self.frame )

    def render_tcs( self, origin, size ):
        """
        Renders the texture coordinates.

        If rendered over a blit of the texture used and
        scaled to the same size, this can be used to
        display the texture coordinates used visually.
        """
        x = origin[ 0 ]
        y = origin[ 1 ]
        width = size[ 0 ]
        height = size[ 1 ]

        glPushAttrib( GL_ALL_ATTRIB_BITS )

        # we want to draw just the lines of the triangles
        # so change our polymode to line only
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        # draw an ourline of the texture
        glBegin( GL_QUADS )
        glVertex2f( 0.0 + x, 0.0 + y )
        glVertex2f( 0.0 + x, height + y )
        glVertex2f( width + x, height + y )
        glVertex2f( width + x, 0.0 + y )
        glEnd()

        # find the TCs for each triangle
        tcs_triangles = numpy.array( self.md2.tcs )
        tcs_triangles *= size
        tcs_triangles += origin

        # pass to opengl
        pyglet.graphics.draw(
            len( tcs_triangles ),
            GL_TRIANGLES,
            ('v2f/static', tcs_triangles.flatten())
            )

        glPopAttrib()

