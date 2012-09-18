'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>

.. todo:: rotate by matrix
.. todo:: rotate by eulers
.. todo:: rotate_about_axis( axis, radians )
.. todo:: look_at_world
.. todo:: look_at_local
.. todo:: look_at_inertial
'''

import weakref

import numpy
from pyglet.gl import *

from pyrr import quaternion
from pyrr import matrix33
from pyrr import matrix44
from tree_node import TreeNode
from transform import Transform
from world_transform import WorldTransform

    
class SceneNode( TreeNode ):
    """Base class for Scene Graph objects.
    """
    
    def __init__( self, name ):
        """Creates a SceneNode object with the specified name.
        """
        super( SceneNode, self ).__init__()

        #: The name of the node.
        self.name = name
        
        #: The local transform of the node.
        self.transform = Transform()
        #: The world transform of the node.
        self.world_transform = WorldTransform( self.transform )

        # listen for new parents and children
        self.push_handlers(
            on_parent_changed = self._on_parent_changed
            )

    def _on_parent_changed( self, old_parent, new_parent ):
        """Event handler for TreeNode's parent events.

        Manages the addition and removal of our world
        transform from our parent.
        """
        if old_parent != None:
            old_parent.world_transform.remove_child(
                self.world_transform
                )
        if new_parent != None:
            new_parent.world_transform.add_child(
                self.world_transform
                )

