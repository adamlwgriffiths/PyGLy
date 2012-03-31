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

import maths.quaternion
import maths.matrix33
import maths.matrix44
import debug_cube
import debug_axis


    
class SceneNode( object ):
    """
    Base class for Scene Graph objects.
    """
    
    """
    If set to true, each scene node will
    render a debug cube to show its
    position within the scene.
    """
    debug = False

    def __init__( self, name ):
        super( SceneNode, self ).__init__()
        
        self.name = name
        
        self._parent = None
        self.children = set()
        
        self._orientation = maths.quaternion.identity()        
        self._world_orientation = maths.quaternion.identity()
        
        self._translation = numpy.zeros( 3, dtype = float )
        self._world_translation = numpy.zeros( 3, dtype = float )
        
        self.scale = numpy.ones( (3), dtype = float )
        self.dirty = True

    def _set_dirty( self ):
        self.dirty = True
        
        # mark our children as dirty
        for child in self.children:
            child._set_dirty()
    
    def _update_world_translations( self ):
        if self.dirty == False:
            return
        
        parent = self.parent
        if parent == None:
            # no parent
            # just use our local translations
            self._world_translation = self._translation
            self._world_orientation = self._orientation
        else:
            # get our parent's world translation
            parent_world_translation = parent._get_world_translation()
            parent_world_orientation = parent._get_world_orientation()
            
            # rotate our translation by our parent's world orientation
            parent_world_matrix = maths.matrix33.from_inertial_to_object_quaternion( parent_world_orientation )
            world_translation = maths.matrix33.inertial_to_object( self._translation, parent_world_matrix )
            self._world_translation[:] = parent_world_translation + world_translation
            
            # multiply our rotation by our parents
            self._world_orientation = maths.quaternion.cross_product(
                self._orientation,
                parent_world_orientation
                )
        self.dirty = False
    
    def _get_local_translation( self ):
        return self._translation
    
    def _set_local_translation( self, translation ):
        # check for the translation not changing
        if numpy.array_equal( translation, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        self._translation[:] = translation
        self._set_dirty()
    
    translation = property( _get_local_translation, _set_local_translation )
    
    def _get_world_translation( self ):
        if self.dirty == False:
            # world translation is up to date
            return self._world_translation
        else:
            # world translations are dirty
            # update them
            self._update_world_translations()
            return self._world_translation
    
    def _set_world_translation( self, translation ):
        raise NotImplementedError(
            "SceneNode._set_world_translation not implemented for non local translations"
            )
    
    world_translation = property( _get_world_translation, _set_world_translation )
    
    def _get_local_orientation( self ):
        return self._orientation
    
    def _set_local_orientation( self, orientation ):
        # check for the orientation not changing
        if numpy.array_equal( self._orientation, orientation ):
            # don't bother to update anything
            return
        
        self._orientation[:] = orientation
        self._set_dirty()
    
    orientation = property( _get_local_orientation, _set_local_orientation )
    
    def _get_world_orientation( self ):
        if self.dirty == False:
            return self._world_orientation
        else:
            # world translations are dirty
            # update them
            self._update_world_translations()
            return self._world_orientation
    
    def _set_world_orientation( self, orientation ):
        self._set_dirty()
        raise NotImplementedError(
            "SceneNode._setWorldOrientation not implemented"
            )
    
    world_orientation = property( _get_world_orientation, _set_world_orientation )
    
    def rotate_quaternion( self, orientation ):
        # check for the orientation not changing
        if numpy.array_equal( orientation, [ 1.0, 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        # order of operations matters here
        # our orientation must be the second parameter
        maths.quaternion.cross_product(
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
        quat = maths.quaternion.set_to_rotation_about_x( radians )
        self.rotate_quaternion( quat )

    def rotate_object_y( self, radians ):
        """
        Yaw the node about it's Y axis.

        Amount > 0 == yaw right.
        Amount < 0 == yaw left.
        """
        quat = maths.quaternion.set_to_rotation_about_y( radians )
        self.rotate_quaternion( quat )
    
    def rotate_object_z( self, radians ):
        """
        Roll the node about it's Z axis.

        Amount > 0 == roll left.
        Amount < 0 == roll right.
        """
        quat = maths._quaternion.set_to_rotation_about_z( radians )
        self.rotate_quaternion( quat )

    def _rotate_vector_by_quaternion( self, quat, vec ):
        matrix = maths.matrix33.from_inertial_to_object_quaternion( quat )
        result_vec = maths.matrix33.inertial_to_object( vec, matrix )
        return result_vec

    def object_x_axis( self ):
        """
        Returns the object's local X axis.
        This is the X axis rotated by the objects
        orientation. This is NOT the world orientation.
        To get inertial X axis, simply use [1.0, 0.0, 0.0].
        """
        return self._rotate_vector_by_quaternion(
            self.orientation,
            [1.0, 0.0, 0.0]
            )

    def object_y_axis( self ):
        """
        Returns the object's local Y axis.
        This is the Y axis rotated by the objects
        orientation. This is NOT the world orientation.
        To get inertial Y axis, simply use [0.0, 1.0, 0.0].
        """
        return self._rotate_vector_by_quaternion(
            self.orientation,
            [0.0, 1.0, 0.0]
            )

    def object_z_axis( self ):
        """
        Returns the object's local Z axis.
        This is the Z axis rotated by the objects
        orientation. This is NOT the world orientation.
        To get inertial Z axis, simply use [0.0, 0.0, 1.0].
        """
        return self._rotate_vector_by_quaternion(
            self.orientation,
            [0.0, 0.0, 1.0]
            )

    def world_x_axis( self ):
        """
        Returns the object's world X axis.
        """
        return self._rotate_vector_by_quaternion(
            self.world_orientation,
            [1.0, 0.0, 0.0]
            )

    def world_y_axis( self ):
        """
        Returns the object's world Y axis.
        """
        return self._rotate_vector_by_quaternion(
            self.world_orientation,
            [0.0, 1.0, 0.0]
            )

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
        # apply the translation
        self._translation += vec
        self._set_dirty()

    def translate_inertial_x( self, amount ):
        """
        Translates the node along it's inertial X axis.
        The inertial axis of the object does not include
        it's local orientation.
        """
        self._translation += [ float(amount), 0.0, 0.0 ]
        self._set_dirty()

    def translate_inertial_y( self, amount ):
        """
        Translates the node along it's inertial Y axis.
        The inertial axis of the object does not include
        it's local orientation.
        """
        self._translation += [ 0.0, float(amount), 0.0 ]
        self._set_dirty()

    def translate_inertial_z( self, amount ):
        """
        Translates the node along it's inertial Z axis.
        The inertial axis of the object does not include
        it's local orientation.
        """
        self._translation += [ 0.0, 0.0, float(amount) ]
        self._set_dirty()
    
    def translate_object( self, vec ):
        """
        Translates the node locally.
        The vector will have the node's current orientation
        applied to it and then be added to the translation.
        """
        # multiply the vector by our local orientation
        localVec = self._rotate_vector_by_quaternion( self.orientation, vec )

        # apply the translation
        self._translation += localVec
        self._set_dirty()
    
    def translate_object_x( self, amount ):
        """
        Translates the node forward or backward along
        it's local X axis.

        +X is right.
        -X is left.
        """
        if amount == 0.0:
            return
        
        vec = [float(amount), 0.0, 0.0]
        self.translate_object( vec )
    
    def translate_object_y( self, amount ):
        """
        Translates the node upward or downward along
        it's local Y axis.

        +Y is upward.
        -Y is downward
        """
        if amount == 0.0:
            return
        
        vec = [0.0, float(amount), 0.0]
        self.translate_object( vec )
    
    def translate_object_z( self, amount ):
        """
        Translates the node forward or backward along
        it's local Z axis.

        +Z is backward.
        -Z is forward.
        """
        if amount == 0.0:
            return
        
        vec = [0.0, 0.0, float(amount)]
        self.translate_object( vec )
    
    def set_scale( self, scale ):
        """
        Sets the current scale.
        """
        self.scale[:] = scale

    def apply_scale( self, scale ):
        """
        Multiplies the existing scale by the
        specified value.
        """
        self.scale *= scale
    
    def add_child( self, node ):
        """
        Attaches a child to the node.
        """
        previous_parent = node.parent
        if previous_parent != None:
            previous_parent.remove_child( node )
        
        # add the node
        self.children.add( node )
        
        # set ourself as the parent
        node._parent = weakref.ref( self )
        
        # mark the node as dirty
        node._set_dirty()
    
    def remove_child( self, node ):
        """
        Removes a child from the node.

        @raise KeyError: Raised if the node
        is not a child of the node.
        """
        # remove from our list of children
        self.children.remove( node )
        # unset the node's parent
        node._parent = None
        # mark the node as dirty
        node._set_dirty()
    
    @property
    def parent( self ):
        """
        A property accessable as a member.
        Returns the parent of the node or None
        if there isn't one.
        """
        if self._parent != None:
            return self._parent()
        return None
    
    def on_context_lost( self ):
        """
        Called when the window loses it's graphical
        context.
        TODO: This needs to be replaced with a per-window
        call, not per tree. As there can be multiple
        windows. Moving windows across desktops can
        trigger this.
        """
        # TODO: replace this with a mesh pool or event callback
        # that does this for only objects that need it

        # we don't need to do anything
        # but our children might
        for child in self.children:
            child.on_context_lost()
    
    def apply_translations( self ):
        """
        Applies the node's translation, orientation and
        scale to the current opengl matrix.
        Does NOT call glPushMatrix or glPopMatrix.
        """
        # matrix transformations must be done in order
        # orientation and scaling
        # finally translation

        # convert our quaternion to a matrix
        matrix = maths.matrix44.from_inertial_to_object_quaternion(
            self._orientation
            )

        # apply our scale
        maths.matrix44.scale( matrix, self.scale, matrix )

        # apply our translation
        # we MUST do this after the orientation
        maths.matrix44.set_translation( matrix, self._translation, out = matrix )
        
        # convert to ctype for OpenGL
        glMatrix = (GLfloat * matrix.size)(*matrix.flat) 
        glMultMatrixf( glMatrix )
    
    def render( self ):
        """
        Does the following in order:
         Pushes the current gl matrix.
         Applies the node's translations.
         Renders debug info if enabled.
         Calls 'render' on all children.
         Pops the gl matrix.
        """
        # apply our transforms
        glPushMatrix()
        self.apply_translations()
        
        # check if we should render some debug info
        if SceneNode.debug == True:
            self.render_debug_info()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()

    def render_debug_info( self ):
        """
        Renders debug information at the current
        gl translation.
        """
        # render any debug info
        debug_cube.render()
        debug_axis.render()
    


if __name__ == "__main__":
    import common.list
    import math

    def compare_float_vector( a, b, tolerance = 0.1 ):
        for i, j in zip( a, b ):
            if (i - tolerance) > j:
                return False
            if (i + tolerance) < j:
                return False
        return True
    # test our above test function
    # test-ception
    assert compare_float_vector( [1.0,0.0], [1.0,0.0] )
    assert compare_float_vector( [1.0,0.0], [0.0,1.0] ) == False
    assert compare_float_vector( [1.0,0.0], [1.01,0.0] )
    assert compare_float_vector( [1.0,0.0], [1.11,0.0] ) == False

    """
    Tree methods
    """
    root = SceneNode( 'root' )
    
    child1_1 = SceneNode( 'child1_1' )
    child1_2 = SceneNode( 'child1_2' )
    
    child2_1 = SceneNode( 'child2_1' )
    child2_2 = SceneNode( 'child2_2' )
    
    root.add_child( child1_1 )
    root.add_child( child1_2 )
    
    child1_1.add_child( child2_1 )
    child1_2.add_child( child2_2 )
    
    assert child1_1.parent is root
    assert child1_1 in root.children
    assert child1_2.parent is root
    assert child1_2 in root.children
    
    assert child2_1.parent is child1_1
    assert child2_1 in child1_1.children
    assert child2_2.parent is child1_2
    assert child2_2 in child1_2.children
    
    child1_1.add_child( child2_2 )
    
    assert child2_2.parent is child1_1
    assert child2_2 in child1_1.children
    assert child2_2 not in child1_2.children
    
    """
    Rotation and Inheritance
    """

    # we'll add a child to a root node
    # we'll move the child
    # rotate the root
    # and check the child is where it should be
    # the child should be moved somewhere that will
    # make it easy to check

    root = SceneNode( '/root' )
    assert common.list.are_equivalent(root.object_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(root.object_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(root.object_z_axis(), [0.0,0.0,1.0])
    assert common.list.are_equivalent(root.world_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(root.world_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(root.world_z_axis(), [0.0,0.0,1.0])

    child = SceneNode( '/child' )
    assert common.list.are_equivalent(child.object_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(child.object_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(child.object_z_axis(), [0.0,0.0,1.0])
    assert common.list.are_equivalent(child.world_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(child.world_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(child.world_z_axis(), [0.0,0.0,1.0])

    root.add_child( child )
    assert common.list.are_equivalent(root.object_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(root.object_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(root.object_z_axis(), [0.0,0.0,1.0])
    assert common.list.are_equivalent(root.world_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(root.world_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(root.world_z_axis(), [0.0,0.0,1.0])
    assert common.list.are_equivalent(child.object_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(child.object_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(child.object_z_axis(), [0.0,0.0,1.0])
    assert common.list.are_equivalent(child.world_x_axis(), [1.0,0.0,0.0])
    assert common.list.are_equivalent(child.world_y_axis(), [0.0,1.0,0.0])
    assert common.list.are_equivalent(child.world_z_axis(), [0.0,0.0,1.0])

    # rotate 180 deg / 1pi about the y axis (yaw)
    root.rotate_object_y( math.pi )
    # ensure the object x axis has rotated to the left
    assert compare_float_vector(root.object_x_axis(), [-1.0,0.0,0.0])
    assert compare_float_vector(root.object_y_axis(), [0.0,1.0,0.0])
    assert compare_float_vector(root.object_z_axis(), [0.0,0.0,-1.0])
    assert compare_float_vector(root.world_x_axis(), [-1.0,0.0,0.0])
    assert compare_float_vector(root.world_y_axis(), [0.0,1.0,0.0])
    assert compare_float_vector(root.world_z_axis(), [0.0,0.0,-1.0])
    # ensure the child's object x axis has remaind unchanged
    assert compare_float_vector(child.object_x_axis(), [1.0,0.0,0.0])
    assert compare_float_vector(child.object_y_axis(), [0.0,1.0,0.0])
    assert compare_float_vector(child.object_z_axis(), [0.0,0.0,1.0])
    assert compare_float_vector(child.world_x_axis(), [-1.0,0.0,0.0])
    assert compare_float_vector(child.world_y_axis(), [0.0,1.0,0.0])
    assert compare_float_vector(child.world_z_axis(), [0.0,0.0,-1.0])

    # rotate 180 deg / 1pi about the x axis (pitch)
    root.rotate_object_x( math.pi )
    # ensure the object y axis has inverted to the bottom
    # the z axis will have inverted again
    assert compare_float_vector(root.object_x_axis(), [-1.0,0.0,0.0])
    assert compare_float_vector(root.object_y_axis(), [0.0,-1.0,0.0])
    assert compare_float_vector(root.object_z_axis(), [0.0,0.0,1.0])
    assert compare_float_vector(root.world_x_axis(), [-1.0,0.0,0.0])
    assert compare_float_vector(root.world_y_axis(), [0.0,-1.0,0.0])
    assert compare_float_vector(root.world_z_axis(), [0.0,0.0,1.0])
    # ensure the child's object y axis has remaind unchanged
    assert compare_float_vector(child.object_x_axis(), [1.0,0.0,0.0])
    assert compare_float_vector(child.object_y_axis(), [0.0,1.0,0.0])
    assert compare_float_vector(child.object_z_axis(), [0.0,0.0,1.0])
    assert compare_float_vector(child.world_x_axis(), [-1.0,0.0,0.0])
    assert compare_float_vector(child.world_y_axis(), [0.0,-1.0,0.0])
    assert compare_float_vector(child.world_z_axis(), [0.0,0.0,1.0])


    """
    Scale
    """
    root = SceneNode( '/root' )
    assert common.list.are_equivalent(root.scale, [1.0,1.0,1.0])
    root.set_scale( [2.0, 2.0, 2.0] )
    assert common.list.are_equivalent(root.scale, [2.0,2.0,2.0])
    root.set_scale( [1.0, 1.0, 1.0] )
    assert common.list.are_equivalent(root.scale, [1.0,1.0,1.0])
    root.apply_scale( [2.0, 2.0, 2.0] )
    assert common.list.are_equivalent(root.scale, [2.0,2.0,2.0])
    root.apply_scale( [2.0, 2.0, 2.0] )
    assert common.list.are_equivalent(root.scale, [4.0,4.0,4.0])

