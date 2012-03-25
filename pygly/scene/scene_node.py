'''
Created on 20/06/2011

@author: adam
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
        
        maths.quaternion.cross_product(
            self._orientation,
            orientation,
            out = self._orientation
            )
        self._set_dirty()
    
    def rotate_matrix( self, orientation ):
        # TODO: check for identity matrix
        # check for the orientation not changing
        self._set_dirty()
        raise NotImplementedError(
            "SceneNode.rotate_matrix not implemented for non local translations"
            )
    
    def rotate_eulers( self, orientation ):
        self._set_dirty()
        raise NotImplementedError(
            "SceneNode.rotate_eulers not implemented for non local translations"
            )
    
    def rotate_about_axis( self, radians, axis ):
        self._set_dirty()
        raise NotImplementedError(
            "SceneNode.rotateAboutAxis not implemented for non local translations"
            )
    
    def pitch( self, amount ):
        """
        Amount > 0 == pitch down
        Amount < 0 == pitch up
        """
        pitch_quat = maths.quaternion.set_to_rotation_about_x( amount )
        self.rotate_quaternion( pitch_quat )
    
    def pitch_forward( self, amount ):
        self.pitch( amount )
    
    def pitch_backward( self, amount ):
        self.pitch( -amount )
    
    def yaw( self, amount ):
        """
        Amount < 0 == yaw left.
        Amount > 0 == yaw right.
        """
        yaw_quat = maths.quaternion.set_to_rotation_about_y( amount )
        self.rotate_quaternion( yaw_quat )
    
    def yaw_right( self, amount ):
        self.yaw( -amount )
    
    def yaw_left( self, amount ):
        self.yaw( amount )
    
    def roll( self, amount ):
        roll_quat = maths._quaternion.set_to_rotation_about_z( amount )
        self.rotate_quaternion( roll_quat )
    
    def roll_right( self, amount ):
        self.roll( -amount )
    
    def roll_left( self, amount ):
        self.roll( amount )
        
    def look_at_world( self, target, upAxis ):
        self._set_dirty()
        raise NotImplementedError(
            "SceneNode.lookAt not implemented for non local translations"
            )
    
    def translate( self, vector ):
        self._translation += vector
        self._set_dirty()
    
    def translate_forward( self, amount ):
        if amount == 0.0:
            return
        
        matrix = maths.matrix33.from_inertial_to_object_quaternion( self._orientation )
        forwardVec = maths.matrix33.inertial_to_object( [ 0.0, 0.0, -1.0 ], matrix )
        forwardVec *= amount
        self.translate( forwardVec )
    
    def translate_backward( self, amount ):
        self.translate_forward( -amount )
    
    def translate_right( self, amount ):
        if amount == 0.0:
            return
        
        matrix = maths.matrix33.from_inertial_to_object_quaternion( self._orientation )
        rightVec = maths.matrix33.inertial_to_object( [ 1.0, 0.0, 0.0 ], matrix )
        rightVec *= amount
        self.translate( rightVec )
    
    def translate_left( self, amount ):
        self.translate_right( -amount )
    
    def translate_up( self, amount ):
        if amount == 0.0:
            return
        
        matrix = maths.matrix33.from_inertial_to_object_quaternion( self._orientation )
        upVec = maths.matrix33.inertial_to_object( [ 0.0, 1.0, 0.0 ], matrix )
        upVec *= amount
        self.translate( upVec )
    
    def translate_down( self, amount ):
        self.translate_up( -amount )
    
    def set_scale( self, scale ):
        self.scale[:] = scale
    
    def add_child( self, node ):
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
        # remove from our list of children
        self.children.remove( node )
        # unset the node's parent
        node._parent = None
        # mark the node as dirty
        node._set_dirty()
    
    @property
    def parent( self ):
        if self._parent != None:
            return self._parent()
        return None
    
    def on_context_lost( self ):
        # TODO: replace this with a mesh pool or event callback
        # that does this for only objects that need it

        # we don't need to do anything
        # but our children might
        for child in self.children:
            child.on_context_lost()
    
    def apply_translations( self ):
        # convert our quaternion to a matrix
        matrix = maths.matrix44.from_inertial_to_object_quaternion( self._orientation )
        
        # add our translation to the matrix
        maths.matrix44.set_translation( matrix, self._translation, out = matrix )

        # apply our scale
        maths.matrix44.scale( matrix, self.scale, out = matrix )
        
        # convert to ctype for OpenGL
        glMatrix = (GLfloat * matrix.size)(*matrix.flat) 
        glMultMatrixf( glMatrix )
    
    def render( self ):
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
        # render any debug info
        debug_cube.render()
        debug_axis.render()
    


if __name__ == "__main__":
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
    

