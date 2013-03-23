import pyrr.rectangle
import pyrr.matrix44

import scene_scene_graph


class Scene( scene_scene_graph.Scene ):

    def __init__( self, core_profile = True ):
        super( Scene, self ).__init__( core_profile )

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
        half_width = (width / 2.0) / 10.0
        half_height = (height / 2.0) / 10.0
        aspect_ratio = pyrr.rectangle.aspect_ratio( self.viewport )
        self.camera.projection_matrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            left = -half_width,
            right = half_width,
            top = half_height,
            bottom = -half_height,
            near = 1.0,
            far = 200.0
            )
