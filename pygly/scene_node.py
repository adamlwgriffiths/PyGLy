'''
Created on 20/06/2011

@author: adam

TODO: rotate by matrix
TODO: rotate by eulers
TODO: rotate_about_axis( axis, radians )
TODO: look_at_world
TODO: look_at_local
TODO: look_at_inertial
'''

import weakref

import numpy
from pyglet.gl import *

from pyrr import quaternion
from pyrr import matrix33
from pyrr import matrix44
from tree_node import TreeNode
import debug_cube
import debug_axis


    
class SceneNode( TreeNode ):
    """
    Base class for Scene Graph objects.
    """
    
    def __init__( self, name ):
        super( SceneNode, self ).__init__()

        self.name = name
        
        self._orientation = quaternion.identity()        
        self._world_orientation = quaternion.identity()
        
        self._translation = numpy.zeros( 3, dtype = numpy.float )
        self._world_translation = numpy.zeros( 3, dtype = numpy.float )
        
        self._scale = numpy.ones( 3, dtype = numpy.float )
        self._world_scale = numpy.ones( 3, dtype = numpy.float )

        self._world_matrix = matrix44.identity()

        self.dirty = True

    def _set_dirty( self ):
        """
        Marks the node and all children as 'dirty'.
        A 'dirty' node is one that needs to have its
        world translation and orientation updated.
        """
        self.dirty = True
        
        # mark our children as dirty
        for child in self.children:
            if hasattr( child, '_set_dirty' ):
                child._set_dirty()
    
    def _update_world_translations( self ):
        """
        Called on 'dirty' nodes.
        Re-calculates the node's world orientation and
        translation based upon the node's parent and its
        own orientation and translation.
        """
        if self.dirty == False:
            return
        
        if self.parent == None:
            # no parent
            self._world_translation[:] = self.inertial_translation
            self._world_orientation[:] = self.object_orientation
            self._world_scale[:] = self.scale
            self._world_matrix[:] = self.object_matrix
        else:
            # rotate our translation by our parent's
            # world orientation
            parent_world_matrix = self.parent.world_matrix

            # calculate our world scale
            self._world_scale = self.scale * self.parent.world_scale

            # multiply our rotation by our parents
            # order is important, our quaternion should
            # be the second parameter
            self._world_orientation = quaternion.cross(
                self.parent.world_orientation,
                self.object_orientation
                )

            # apply to our translation
            world_translation = matrix33.apply_to_vector(
                self.inertial_translation,
                parent_world_matrix
                )

            self._world_translation[:] = \
                self.parent.world_translation + world_translation

            matrix44.multiply(
                self.object_matrix,
                self.parent.world_matrix,
                out = self._world_matrix
                )
            
        self.dirty = False
    
    @property
    def inertial_translation( self ):
        """
        Returns the current inertial translation.
        """
        return self._translation
    
    @inertial_translation.setter
    def inertial_translation( self, translation ):
        """
        Sets the inertial translation of the node.
        """
        # check for the translation not changing
        if numpy.array_equal( translation, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        self._translation[:] = translation
        self._set_dirty()
    
    @property
    def world_translation( self ):
        """
        Returns the node's world translation.

        If the node is marked as 'dirty', will
        automatically call _update_world_translations
        and return the calculated value.
        """
        if self.dirty == False:
            # world translation is up to date
            return self._world_translation
        else:
            # world translations are dirty
            # update them
            self._update_world_translations()
            return self._world_translation
    
    @property
    def object_orientation( self ):
        """
        Returns the node's object orientation
        """
        return self._orientation
    
    @object_orientation.setter
    def object_orientation( self, orientation ):
        """
        Stores the node's object orientation
        """
        # check for the orientation not changing
        if numpy.array_equal( self._orientation, orientation ):
            # don't bother to update anything
            return
        
        self._orientation[:] = orientation
        self._set_dirty()
    
    @property
    def world_orientation( self ):
        """
        Returns the node's world orientation.

        Automatically calls _update_world_translations
        if the node is marked as 'dirty' and returns
        the calculated result.
        """
        if self.dirty == False:
            return self._world_orientation
        else:
            # world translations are dirty
            # update them
            self._update_world_translations()
            return self._world_orientation

    @property
    def scale( self ):
        return self._scale

    @scale.setter
    def scale( self, scale ):
        if numpy.array_equal( scale, [ 1.0, 1.0, 1.0 ] ):
            # don't bother to update anything
            return

        self._scale[:] = scale
        self._set_dirty()

    @property
    def world_scale( self ):
        """
        Returns the node's world orientation.

        Automatically calls _update_world_translations
        if the node is marked as 'dirty' and returns
        the calculated result.
        """
        if self.dirty == False:
            return self._world_scale
        else:
            # world translations are dirty
            # update them
            self._update_world_translations()
            return self._world_scale

    def rotate_object_quaternion( self, orientation ):
        """
        Rotates the node by the specified orientation.
        The quaternion is in object space.
        """
        # check for the orientation not changing
        if numpy.array_equal( orientation, [ 1.0, 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        # order of operations matters here
        # our orientation must be the second parameter
        quaternion.cross(
            orientation,
            self._orientation,
            out = self._orientation
            )
        self._set_dirty()
    
    def rotate_object_x( self, radians ):
        """
        Pitch the node about it's X axis.

        Amount > 0 == pitch down
        Amount < 0 == pitch up
        """
        if radians == 0.0:
            return

        quat = quaternion.set_to_rotation_about_x( radians )
        self.rotate_object_quaternion( quat )

    def rotate_object_y( self, radians ):
        """
        Yaw the node about it's Y axis.

        Amount > 0 == yaw right.
        Amount < 0 == yaw left.
        """
        if radians == 0.0:
            return

        quat = quaternion.set_to_rotation_about_y( radians )
        self.rotate_object_quaternion( quat )
    
    def rotate_object_z( self, radians ):
        """
        Roll the node about it's Z axis.

        Amount > 0 == roll left.
        Amount < 0 == roll right.
        """
        if radians == 0.0:
            return

        quat = quaternion.set_to_rotation_about_z( radians )
        self.rotate_object_quaternion( quat )

    def _rotate_vector_by_quaternion( self, quat, vec ):
        matrix = matrix33.create_from_quaternion( quat )
        result_vec = matrix33.apply_to_vector( vec, matrix )
        return result_vec

    @property
    def object_x_axis( self ):
        """
        Returns the object's local X axis.
        This is the X axis rotated by the objects
        orientation. This is NOT the world orientation.
        To get inertial X axis, simply use [1.0, 0.0, 0.0].
        """
        return self._rotate_vector_by_quaternion(
            self.object_orientation,
            [1.0, 0.0, 0.0]
            )

    @property
    def object_y_axis( self ):
        """
        Returns the object's local Y axis.
        This is the Y axis rotated by the objects
        orientation. This is NOT the world orientation.
        To get inertial Y axis, simply use [0.0, 1.0, 0.0].
        """
        return self._rotate_vector_by_quaternion(
            self.object_orientation,
            [0.0, 1.0, 0.0]
            )

    @property
    def object_z_axis( self ):
        """
        Returns the object's local Z axis.
        This is the Z axis rotated by the objects
        orientation. This is NOT the world orientation.
        To get inertial Z axis, simply use [0.0, 0.0, 1.0].
        """
        return self._rotate_vector_by_quaternion(
            self.object_orientation,
            [0.0, 0.0, 1.0]
            )

    @property
    def world_x_axis( self ):
        """
        Returns the object's world X axis.
        """
        return self._rotate_vector_by_quaternion(
            self.world_orientation,
            [1.0, 0.0, 0.0]
            )

    @property
    def world_y_axis( self ):
        """
        Returns the object's world Y axis.
        """
        return self._rotate_vector_by_quaternion(
            self.world_orientation,
            [0.0, 1.0, 0.0]
            )

    @property
    def world_z_axis( self ):
        """
        Returns the object's world Z axis.
        """
        return self._rotate_vector_by_quaternion(
            self.world_orientation,
            [0.0, 0.0, 1.0]
            )

    def translate_inertial( self, vec ):
        """
        Translates the node along it's inertial axis.
        The inertial axis of the object does not include
        it's local orientation.
        """
        if numpy.array_equal( vec, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return

        # apply the translation
        self._translation += vec
        self._set_dirty()

    def translate_inertial_axis( self, x = 0.0, y = 0.0, z = 0.0 ):
        """
        Translates the node along it's inertial axis.
        The inertial axis of the object does not include
        it's local orientation.
        """
        self.translate_inertial( [ float(x), float(y), float(z) ] )
    
    def translate_object( self, vec ):
        """
        Translates the node locally.
        The vector will have the node's current orientation
        applied to it and then be added to the translation.
        """
        if numpy.array_equal( vec, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return

        # multiply the vector by our local orientation
        localVec = self._rotate_vector_by_quaternion(
            self.object_orientation,
            vec
            )

        # apply the translation
        self._translation += localVec
        self._set_dirty()
    
    def translate_object_axis( self, x = 0.0, y = 0.0, z = 0.0 ):
        """
        Translates the node locally.
        The vector will have the node's current orientation
        applied to it and then be added to the translation.
        """
        self.translate_object( [float(x), float(y), float(z)] )
    
    def add_child( self, node ):
        """
        Attaches a child to the node.
        """
        super( SceneNode, self ).add_child( node )
        
        # mark the node as dirty
        if hasattr( node, '_set_dirty' ):
            node._set_dirty()
    
    def remove_child( self, node ):
        """
        Removes a child from the node.

        @raise KeyError: Raised if the node
        is not a child of the node.
        """
        super( SceneNode, self ).remove_child( node )

        # mark the node as dirty
        if hasattr( node, '_set_dirty' ):
            node._set_dirty()
    
    @property
    def object_matrix( self ):
        """
        Returns a matrix representing the node's
        object translation, orientation and
        scale.
        """
        # matrix transformations must be done in order
        # scaling
        # rotation
        # translation

        # apply our scale
        matrix = matrix44.create_from_scale( self.scale )

        # apply our quaternion
        matrix44.multiply(
            matrix,
            matrix44.create_from_quaternion(
                self.object_orientation
                ),
            out = matrix
            )

        # apply our translation
        # we MUST do this after the orientation
        matrix44.multiply(
            matrix,
            matrix44.create_from_translation(
                self.inertial_translation,
                ),
            out = matrix
            )

        return matrix

    @property
    def world_matrix( self ):
        """
        Returns a matrix representing the node's
        world translation, orientation and
        scale.
        """
        if self.parent == None:
            return self.object_matrix
        else:
            if self.dirty == True:
                self._update_world_translations()
            return self._world_matrix
    
    def render_debug( self ):
        """
        Does the following in order:
         Pushes the current gl matrix.
         Applies the node's translations.
         Renders debug info.
         Calls this method on all child nodes.
         Pops the gl matrix.
        """
        # store the existing matrix state
        glPushMatrix()

        # apply our transforms
        matrix = self.world_matrix
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

