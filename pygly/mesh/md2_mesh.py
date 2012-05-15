# -*- coding: utf-8 -*-
"""
Created on 02/04/2012

@author: adam
"""

from md2_renderer import MD2_Renderer


class MD2_Mesh( object ):
    """
    Provides the ability to load and render an MD2
    mesh.

    Uses MD2 to load MD2 mesh data.
    Loads mesh data onto the graphics card to speed
    up rendering. Allows for pre-baking the interpolation
    of frames.
    """
    
    def __init__( self, md2_renderer ):
        """
        Loads an MD2 from the specified file.

        @param md2_renderer: The MD2_Renderer object.
        This is seperated from the MD2_Mesh so that
        you can have multiple meshes with a single
        renderer. That way you don't have to load
        and interpolate an MD2 multiple times.
        """
        super( MD2_Mesh, self ).__init__()
        
        self.frame = 0.0

        self.md2_renderer = md2_renderer

    @property
    def num_frames( self ):
        return self.md2_renderer.num_frames

    def load( self ):
        """
        Reads the MD2 data from the existing
        specified filename.
        """
        self.md2_renderer.load()

    def render( self ):
        """
        Renders the currently set frame.
        """
        # render the vertex list
        self.md2_renderer.render( self.frame )

    def render_tcs( self, origin, size ):
        """
        Renders the texture coordinates.

        If rendered over a blit of the texture used and
        scaled to the same size, this can be used to
        display the texture coordinates used visually.
        """
        self.md2_renderer.render_tcs( origin, size )

