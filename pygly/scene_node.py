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
        
        self._orientation = quaternion.identity()        
        self._world_orientation = quaternion.identity()
        
        self._translation = numpy.zeros( 3, dtype = float )
        self._world_translation = numpy.zeros( 3, dtype = float )
        
        self.scale = numpy.ones( 3, dtype = float )
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
            parent_world_matrix = matrix33.create_from_quaternion(
                parent_world_orientation
                )
            world_translation = matrix33.apply_to_vector(
                self._translation,
                parent_world_matrix
                )
            self._world_translation[:] = parent_world_translation + world_translation
            
            # multiply our rotation by our parents
            self._world_orientation = quaternion.cross(
                self._orientation,
                parent_world_orientation
                )
        self.dirty = False
    
    def _get_inertial_translation( self ):
        """
        Returns the current inertial translation.
        """
        return self._translation
    
    def _set_inertial_translation( self, translation ):
        """
        Sets the inertial translation of the node.
        """
        # check for the translation not changing
        if numpy.array_equal( translation, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        self._translation[:] = translation
        self._set_dirty()
    
    """
    Property that enables access to the inertial translation
    of the node directly.
    Uses the _get_inertial_translation and
    _set_inertial_translation methods.
    """
    inertial_translation = property(
        _get_inertial_translation,
        _set_inertial_translation
        )
    
    def _get_world_translation( self ):
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
    
    def _set_world_translation( self, translation ):
        raise NotImplementedError(
            "SceneNode._set_world_translation not implemented for non local translations"
            )
    
    world_translation = property(
        _get_world_translation,
        _set_world_translation
        )
    
    def _get_object_orientation( self ):
        """
        Returns the node's object orientation
        """
        return self._orientation
    
    def _set_object_orientation( self, orientation ):
        """
        Stores the node's object orientation
        """
        # check for the orientation not changing
        if numpy.array_equal( self._orientation, orientation ):
            # don't bother to update anything
            return
        
        self._orientation[:] = orientation
        self._set_dirty()
    
    """
    Property that enables access to the node's
    object rotation.
    Uses the _get_object_orientation and
    _set_object_orientation methods.
    """
    object_orientation = property(
        _get_object_orientation,
        _set_object_orientation
        )
    
    def _get_world_orientation( self ):
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
    
    def _set_world_orientation( self, orientation ):
        """
        Set's the node's world orientation.
        """
        self._set_dirty()
        raise NotImplementedError(
            "SceneNode._setWorldOrientation not implemented"
            )
    
    """
    Property that enables access to the node's
    world orientation.
    Uses the _get_world_orientation and
    _set_world_orientation methods.
    """
    world_orientation = property(
        _get_world_orientation,
        _set_world_orientation
        )
    
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
        quat = quaternion.set_to_rotation_about_x( radians )
        self.rotate_object_quaternion( quat )

    def rotate_object_y( self, radians ):
        """
        Yaw the node about it's Y axis.

        Amount > 0 == yaw right.
        Amount < 0 == yaw left.
        """
        quat = quaternion.set_to_rotation_about_y( radians )
        self.rotate_object_quaternion( quat )
    
    def rotate_object_z( self, radians ):
        """
        Roll the node about it's Z axis.

        Amount > 0 == roll left.
        Amount < 0 == roll right.
        """
        quat = quaternion.set_to_rotation_about_z( radians )
        self.rotate_object_quaternion( quat )

    def _rotate_vector_by_quaternion( self, quat, vec ):
        matrix = matrix33.create_from_quaternion( quat )
        result_vec = matrix33.apply_to_vector( vec, matrix )
        return result_vec

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
        localVec = self._rotate_vector_by_quaternion(
            self.object_orientation,
            vec
            )

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
        matrix = matrix44.create_from_quaternion(
            self._orientation
            )

        # apply our scale
        matrix44.scale( matrix, self.scale, matrix )

        # apply our translation
        # we MUST do this after the orientation
        matrix44.set_translation( matrix, self._translation, out = matrix )
        
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

