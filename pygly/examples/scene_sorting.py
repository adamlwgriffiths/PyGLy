import textwrap
import math

from OpenGL import GL
import numpy

import pyrr.rectangle
import pyrr.matrix44
import pygly.gl
import pygly.viewport
from pygly.scene_node import SceneNode
from pygly.camera_node import CameraNode
import pygly.sort

import scene
import renderable_colour_cube


class Scene( scene.Scene ):

    def __init__( self, core_profile = True ):
        super( Scene, self ).__init__( core_profile )

    @property
    def name( self ):
        return "Basic"

    def initialise( self ):
        super( Scene, self ).initialise()

        def set_gl_state():
            # setup our GL state
            # disable z buffer
            # because we're rendering transparent cubes
            GL.glDisable( GL.GL_DEPTH_TEST )

            # enable back face culling
            GL.glEnable( GL.GL_CULL_FACE )
            GL.glCullFace( GL.GL_BACK )

            # enable alpha testing
            GL.glEnable( GL.GL_BLEND )
            GL.glBlendFunc( GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA )

        set_gl_state()

        # create a viewport
        # this will be updated before we begin
        self.viewport = None

        # create a cube to render
        self.cube = renderable_colour_cube.create( self.core_profile )

        def setup_scene():
            # create a scene
            # we'll create the scene as a tree
            # to demonstrate the depth-first iteration
            # technique we will use to render it
            self.scene_root = SceneNode( 'root' )

        setup_scene()

        def setup_camera():
            # create our camera node
            self.camera = CameraNode( 'camera', pyrr.matrix44.create_identity() )
            self.scene_root.add_child( self.camera )

            # move the camera so we're not inside
            # the root scene node's debug cube
            self.camera.transform.object.translate(
                [ 0.0, 30.0, 35.0 ]
                )

            # tilt the camera downward
            self.camera.transform.object.rotate_x(-math.pi / 4.0 )

        setup_camera()

        def create_cubes():
            # create a grid of cubes
            self.grid_root = SceneNode( 'grid_root' )
            self.scene_root.add_child( self.grid_root )
            self.grid_root.transform.scale = [2.0, 2.0, 2.0]

            # create a number of cubes
            # the grid will extend from -5 to +5
            x,z = numpy.mgrid[
                -5:5:11j,
                -5:5:11j
                ]
            x = x.flatten()
            z = z.flatten()

            positions = numpy.vstack(
                (x, numpy.zeros( x.shape ), z )
                )
            positions = positions.T

            # set the distance of the cubes
            # cube is -1 -> 1
            # so distance is 2
            positions *= 2.5

            # store a list of renderables
            self.renderables = []

            for position in positions:
                node = SceneNode( 'node-%s' % position )
                node.transform.inertial.translation = position
                self.grid_root.add_child( node )
                self.renderables.append( node )

            # create a range of colours from 0.1 -> 0.5
            self.cube_colours = numpy.linspace( 0.1, 0.5, len(positions) )
            # make them consistent for RGBA
            self.cube_colours = self.cube_colours.repeat( 4 )
            self.cube_colours.shape = (-1, 4)
            # replace the Blue and Alpha value
            self.cube_colours[:,2] = 0.5
            self.cube_colours[:,3] = 0.5

        create_cubes()

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
        self.camera.projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(
            fovy = 80.0,
            aspect = aspect_ratio,
            near = 1.0,
            far = 100.0
            )

    def step( self, dt ):
        super( Scene, self ).step( dt )

        # setup the scene
        # rotate the scene nodes about their vertical axis
        self.grid_root.transform.object.rotate_y( dt * 0.2 )

    def render( self ):
        super( Scene, self ).render()

        # sort our scene
        # extract the positions of all our renderables
        positions = [
            node.world_transform.translation for node in self.renderables
            ]

        # sort our renderables based on their position
        # from the camera
        # sort based on the -Z axis (the direction the
        # camera faces)
        sorted = pygly.sort.sort_radius_back_to_front(
            self.camera.world_transform.translation,
            -(self.camera.transform.object.z),
            self.renderables,
            positions
            )

        def render_core():
            # activate our viewport
            pygly.viewport.set_viewport( self.viewport )

            projection = self.camera.projection_matrix
            model_view = self.camera.model_view

            for node, colour in zip(sorted, self.cube_colours):
                # get the node's world matrix
                world_matrix = node.world_transform.matrix

                # apply the camera's model view to the node's matrix
                current_mv = pyrr.matrix44.multiply(
                    world_matrix,
                    model_view
                    )

                # render a cube
                self.cube.draw( projection, current_mv, colour )

        def render_legacy():
            # activate our viewport
            pygly.viewport.set_viewport( self.viewport )

            # load our projection matrix
            with pygly.gl.mode_and_matrix(
                GL.GL_PROJECTION,
                self.camera.projection_matrix
                ):
                with pygly.gl.mode_and_matrix(
                    GL.GL_MODELVIEW,
                    self.camera.model_view
                    ):
                    # iterate through the scene graph
                    for node, colour in zip(sorted, self.cube_colours):
                        world_matrix = node.world_transform.matrix

                        # multiply the existing model view matrix
                        # by the model's world matrix
                        # then render a cube
                        with pygly.gl.multiply_matrix( world_matrix ):
                            self.cube.draw( colour )

        # render the scene
        if self.core_profile:
            render_core()
        else:
            render_legacy()

