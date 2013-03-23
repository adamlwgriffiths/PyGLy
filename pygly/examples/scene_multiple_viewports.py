from OpenGL import GL
import pyrr.rectangle
import pyrr.matrix44

import pygly.gl
import pygly.viewport
from pygly.scene_node import SceneNode
from pygly.camera_node import CameraNode

import scene_scene_graph


class Scene( scene_scene_graph.Scene ):

    def __init__( self, core_profile = True ):
        super( Scene, self ).__init__( core_profile )

    def initialise( self ):
        super( Scene, self ).initialise()

        def set_gl_state():
            # setup our GL state
            # enable scissoring for viewports
            GL.glEnable( GL.GL_SCISSOR_TEST )

        set_gl_state()

        self.viewport2 = None

        def setup_camera():
            # add another node that our camera will be under
            # we can rotate this node to show how the cameras work
            self.camera2_parent = SceneNode( 'camera2_parent' )
            self.scene_root.add_child( self.camera2_parent )

            # create our camera node
            self.camera2 = CameraNode( 'camera2', pyrr.matrix44.create_identity() )
            self.camera2_parent.add_child( self.camera2 )

            # place the camera at the same position as the previous one
            #self.camera2.transform.translation = self.camera.transform.translation
            #self.camera2.transform.orientation = self.camera.transform.orientation
            #self.camera2.transform.scale = self.camera.transform.scale

            self.camera2.transform.object.translate(
                [ 0.0, 0.0, 35.0 ]
                )

        setup_camera()

    def on_window_resized( self, width, height ):
        #super( Scene, self ).on_window_resized( width, height )

        def update_viewports():
            half_width = width / 2.0

            # update the viewport
            self.viewport = pyrr.rectangle.create_from_position(
                x = 0,
                y = 0,
                width = half_width,
                height = height
                )

            self.viewport2 = pyrr.rectangle.create_from_position(
                x = half_width,
                y = 0,
                width = half_width,
                height = height
                )

            print self.viewport, self.viewport2

        def update_cameras():
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

            # update the projection matrix
            # we need to do this or the rendering will become skewed with each
            # resize of viewport change
            aspect_ratio = pyrr.rectangle.aspect_ratio( self.viewport2 )
            self.camera2.projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(
                fovy = 80.0,
                aspect = aspect_ratio,
                near = 1.0,
                far = 100.0
                )

        update_viewports()
        update_cameras()

    def step( self, dt ):
        super( Scene, self ).step( dt )

        # setup the scene
        # rotate the scene nodes about their vertical axis
        self.camera2_parent.transform.object.rotate_x( dt )

    def render( self ):
        # render viewport 1
        super( Scene, self ).render()

        # change our clear colour to make it clear where the viewport is
        GL.glClearColor( 1.0, 1.0, 1.0, 1.0 )

        # render the viewport
        self.render_viewport( self.viewport2, self.camera2 )

