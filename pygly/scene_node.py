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
import debug_cube
import debug_axis


    
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
    
    def render_debug( self ):
        """Renders debug information to aid in visualising
        scene graphs.

        Does the following in order:
            #. Pushes the current gl matrix.
            #. Applies the node's translations.
            #. Renders debug info.
            #. Calls this method on all child nodes.
            #. Pops the gl matrix.
        """

        #
        # render the cube
        #

        # store the existing matrix state
        glPushMatrix()

        # apply our transforms
        matrix = self.world_transform.matrix
        glMultMatrixf(
            (GLfloat * matrix.size)(*matrix.flat)
            )
        
        # render some debug info
        debug_cube.render()
        debug_axis.render()

        # undo our transforms
        glPopMatrix()
        
        # continue on to our children
        for child in self.children:
            child.render_debug()

