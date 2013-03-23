import textwrap
import math

from OpenGL import GL

import pyrr.rectangle
import pyrr.matrix44
import pygly.gl
import pygly.viewport
from pygly.scene_node import SceneNode
from pygly.camera_node import CameraNode

import scene
import renderable_cube


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
            # enable z buffer
            GL.glEnable( GL.GL_DEPTH_TEST )

            # enable back face culling
            GL.glEnable( GL.GL_CULL_FACE )
            GL.glCullFace( GL.GL_BACK )

        set_gl_state()

        # create a viewport
        # this will be updated before we begin
        self.viewport = None

        # create a cube to render
        self.cube = renderable_cube.create( self.core_profile )

        def setup_scene():
            # create a scene
            # we'll create the scene as a tree
            # to demonstrate the depth-first iteration
            # technique we will use to render it
            self.scene_root = SceneNode( 'root' )

            # the letter indicates the tier the node
            # is on, a = tier 1, b = tier 2, etc.
            self.a1 = SceneNode( 'a1' )
            self.b1 = SceneNode( 'b1' )
            self.b2 = SceneNode( 'b2' )
            self.c1 = SceneNode( 'c1' )
            self.c2 = SceneNode( 'c2' )
            self.c3 = SceneNode( 'c3' )

            # the tree looks as follows
            #                / c1
            #           / b1 - c2
            # root - a1
            #           \ b2 - c3
            self.scene_root.add_child( self.a1 )
            self.a1.add_child( self.b1 )
            self.a1.add_child( self.b2 )
            self.b1.add_child( self.c1 )
            self.b1.add_child( self.c2 )
            self.b2.add_child( self.c3 )

            # if we set the nodes local scale (transform)
            # it will be affected by the parent's scale.
            # by setting the world scale (world_transform)
            # we are ignoring the parent's scale.
            # re-attaching the node would invalidate this.
            self.a1.world_transform.scale = [2.0, 2.0, 2.0]
            self.b1.world_transform.scale = [1.0, 1.0, 1.0]
            self.b2.world_transform.scale = [1.0, 1.0, 1.0]
            self.c1.world_transform.scale = [0.8, 0.8, 0.8]
            self.c2.world_transform.scale = [0.8, 0.8, 0.8]
            self.c3.world_transform.scale = [0.8, 0.8, 0.8]

            # move our scene nodes
            # leave a1 at the centre
            self.b1.transform.object.translate( [10.0, 0.0, 0.0 ] )
            self.b2.transform.object.translate([-10.0, 0.0, 0.0 ] )
            self.c1.transform.object.translate( [ 5.0, 0.0, 0.0 ] )
            self.c2.transform.object.translate( [-5.0, 0.0, 0.0 ] )
            self.c3.transform.object.translate( [ 5.0, 0.0, 0.0 ] )

            # rotate the our b nodes so they tilting forward
            self.b1.transform.object.rotate_x( math.pi / 4.0 )
            self.b2.transform.object.rotate_x( math.pi / 4.0 )

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
        self.a1.transform.object.rotate_y( dt )
        self.b1.transform.object.rotate_y( dt )
        self.b2.transform.object.rotate_y( dt )
        self.c1.transform.object.rotate_y( dt )
        self.c2.transform.object.rotate_y( dt )
        self.c3.transform.object.rotate_y( dt )

    def render( self ):
        super( Scene, self ).render()

        # this code is split into 2 functions to support the
        # multiple_viewports scene which inherits from this class
        self.render_viewport( self.viewport, self.camera )

    def render_viewport( self, viewport, camera ):
        def render_core():
            projection = camera.projection_matrix
            model_view = camera.model_view

            for node in self.scene_root.dfs():
                if isinstance( node, CameraNode ):
                    continue

                # get the node's world matrix
                world_matrix = node.world_transform.matrix

                # apply the camera's model view to the node's matrix
                current_mv = pyrr.matrix44.multiply(
                    world_matrix,
                    model_view
                    )

                # render a cube
                self.cube.draw( projection, current_mv )

        def render_legacy():
            # load our projection matrix
            with pygly.gl.mode_and_matrix(
                GL.GL_PROJECTION,
                camera.projection_matrix
                ):
                with pygly.gl.mode_and_matrix(
                    GL.GL_MODELVIEW,
                    camera.model_view
                    ):
                    # iterate through the scene graph
                    for node in self.scene_root.dfs():
                        # don't render cameras
                        if isinstance( node, CameraNode ):
                            continue

                        world_matrix = node.world_transform.matrix

                        # multiply the existing model view matrix
                        # by the model's world matrix
                        # then render a cube
                        with pygly.gl.multiply_matrix( world_matrix ):
                            self.cube.draw()

        # activate our viewport
        pygly.viewport.set_viewport( viewport )

        # set our scissor to the main viewport
        pygly.viewport.set_scissor( viewport )

        # clear the colour and depth buffer
        GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT )

        # render the scene
        if self.core_profile:
            render_core()
        else:
            render_legacy()
