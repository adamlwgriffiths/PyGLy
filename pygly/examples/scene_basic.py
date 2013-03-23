import textwrap

from OpenGL import GL

import pyrr.rectangle
import pyrr.matrix44
import pygly.gl
import pygly.viewport

import scene
import renderable_triangle


class Scene( scene.Scene ):

    def __init__( self, core_profile = True ):
        super( Scene, self ).__init__( core_profile )

    @property
    def name( self ):
        return "Basic"

    def initialise( self ):
        super( Scene, self ).initialise()

        # create a viewport
        # this will be updated before we begin
        self.viewport = None

        # create our projection matrix
        # this will be updated before we begin rendering
        self.projection_matrix = None

        # create a triangle to render
        self.triangle = renderable_triangle.create( self.core_profile )

        # move the triangle back
        self.transform = pyrr.matrix44.create_from_translation(
            [ 0.0, 0.0,-3.0 ]
            )

    def on_window_resized( self, width, height ):
        # update the viewport
        self.viewport = pyrr.rectangle.create_from_position(
            x = 0,
            y = 0,
            width = width,
            height = height
            )

        # update the projection matrix
        # we need to do this or the rendering will become skewed with each
        # resize of viewport change
        aspect_ratio = pyrr.rectangle.aspect_ratio( self.viewport )
        self.projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(
            fovy = 80.0,
            aspect = aspect_ratio,
            near = 1.0,
            far = 100.0
            )

    def render( self ):
        super( Scene, self ).render()

        def render_core():
            # activate our viewport
            pygly.viewport.set_viewport( self.viewport )

            self.triangle.draw( self.projection_matrix, self.transform )

        def render_legacy():
            # activate our viewport
            pygly.viewport.set_viewport( self.viewport )

            with pygly.gl.mode_and_matrix(
                GL.GL_PROJECTION,
                self.projection_matrix
                ):
                with pygly.gl.mode_and_matrix(
                    GL.GL_MODELVIEW,
                    self.transform
                    ):
                    self.triangle.draw()

        # setup the projection and model view matrices
        # and draw the triangle
        if self.core_profile:
            render_core()
        else:
            render_legacy()

