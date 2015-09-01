import math

from pyrr import quaternion
from pyrr import matrix44
from pyrr import ray

from scene_node import SceneNode


class CameraNode( SceneNode ):
    """A Scene Graph based camera.
    """
    
    
    def __init__( self, name, projection_matrix ):
        """Creates a CameraNode object.

        :param string name: The name to give to the node.
        :param ProjectionMatrix projection_matrix: The camera's projection matrix.
        """
        super( CameraNode, self ).__init__( name )
        
        #: the camer's view matrix
        self.projection_matrix = projection_matrix

    @property
    def model_view( self ):
        """Property for the camera's model view matrix.

        This is the inverse of the camera's world matrix
        and is used as the initial matrix for the model view
        matrix.

        This is an @property decorated method.

        :rtype: numpy.array
        :return: A matrix set to the camera's model view
            matrix.
        """
        # return the inverse of our world matrix
        return matrix44.inverse( self.world_transform.matrix )
