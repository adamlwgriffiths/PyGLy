'''
Created on 20/06/2011

@author: adam
'''

import weakref

import numpy
from pyglet.gl import *

from Pyrr import Quaternion
from Pyrr import Matrix33
from Pyrr import Matrix44

import DebugCube


    
class SceneNode( object ):
    """
    Base class for Scene Graph objects.
    
    TODO: Add scale inheritance
    """
    
    renderDebugCube = False
    
    
    def __init__( self, name ):
        super( SceneNode, self ).__init__()
        
        self.name = name
        
        self._parent = None
        self.children = set()
        
        self._orientation = Quaternion.identity()        
        self._worldOrientation = Quaternion.identity()
        
        self._translation = numpy.zeros( 3, dtype = float )
        self._worldTranslation = numpy.zeros( 3, dtype = float )
        
        self.scale = numpy.ones( (3), dtype = float )
        self.dirty = True
    
    def _setDirty( self ):
        self.dirty = True
        
        # mark our children as dirty
        for child in self.children:
            child._setDirty()
    
    def _updateWorldTranslations( self ):
        if self.dirty == False:
            return
        
        parent = self.parent
        if parent == None:
            # no parent
            # just use our local translations
            self._worldTranslation = self._translation
            self._worldOrientation = self._orientation
        else:
            # get our parent's world translation
            parentWorldTranslation = parent._getWorldTranslation()
            parentWorldOrientation = parent._getWorldOrientation()
            
            # rotate our translation by our paren't world orientation
            parentWorldMatrix = Matrix33.fromInertialToObjectQuaternion( parentWorldOrientation )
            worldTranslation = Matrix33.inertialToObject( self._translation, parentWorldMatrix )
            self._worldTranslation[:] = parentWorldTranslation + worldTranslation
            
            # multiply our rotation by our parents
            self._worldOrientation = Quaternion.crossProduct(
                self._orientation,
                parentWorldOrientation
                )
        self.dirty = False
    
    def _getLocalTranslation( self ):
        return self._translation
    
    def _setLocalTranslation( self, translation ):
        # check for the translation not changing
        if numpy.array_equal( translation, [ 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        self._translation[:] = translation
        self._setDirty()
    
    translation = property( _getLocalTranslation, _setLocalTranslation )
    
    def _getWorldTranslation( self ):
        if self.dirty == False:
            # world translation is up to date
            return self._worldTranslation
        else:
            # world translations are dirty
            # update them
            self._updateWorldTranslations()
            return self._worldTranslation
    
    def _setWorldTranslation( self, translation ):
        raise NotImplementedError(
            "SceneNode._setWorldTranslation not implemented for non local translations"
            )
    
    worldTranslation = property( _getWorldTranslation, _setWorldTranslation )
    
    def _getLocalOrientation( self ):
        return self._orientation
    
    def _setLocalOrientation( self, orientation ):
        # check for the orientation not changing
        if numpy.array_equal( self._orientation, orientation ):
            # don't bother to update anything
            return
        
        self._orientation[:] = orientation
        self._setDirty()
    
    orientation = property( _getLocalOrientation, _setLocalOrientation )
    
    def _getWorldOrientation( self ):
        if self.dirty == False:
            return self._worldOrientation
        else:
            # world translations are dirty
            # update them
            self._updateWorldTranslations()
            return self._worldOrientation
    
    def _setWorldOrientation( self, orientation ):
        self._setDirty()
        raise NotImplementedError(
            "SceneNode._setWorldOrientation not implemented"
            )
    
    worldOrientation = property( _getWorldOrientation, _setWorldOrientation )
    
    def rotateQuaternion( self, orientation ):
        # check for the orientation not changing
        if numpy.array_equal( orientation, [ 1.0, 0.0, 0.0, 0.0 ] ):
            # don't bother to update anything
            return
        
        Quaternion.crossProduct(
            self._orientation,
            orientation,
            out = self._orientation
            )
        self._setDirty()
    
    def rotateMatrix( self, orientation ):
        # TODO: check for identity matrix
        # check for the orientation not changing
        self._setDirty()
        raise NotImplementedError(
            "SceneNode.rotateAboutAxis not implemented for non local translations"
            )
    
    def rotateEulers( self, orientation ):
        self._setDirty()
        raise NotImplementedError(
            "SceneNode.rotateAboutAxis not implemented for non local translations"
            )
    
    def rotateAboutAxis( self, radians, axis ):
        self._setDirty()
        raise NotImplementedError(
            "SceneNode.rotateAboutAxis not implemented for non local translations"
            )
    
    def pitch( self, amount ):
        """
        Amount > 0 == pitch down
        Amount < 0 == pitch up
        """
        pitchQuat = Quaternion.setToRotationAboutX( amount )
        self.rotateQuaternion( pitchQuat )
    
    def pitchForward( self, amount ):
        self.pitch( amount )
    
    def pitchBackward( self, amount ):
        self.pitch( -amount )
    
    def yaw( self, amount ):
        """
        Amount < 0 == yaw left.
        Amount > 0 == yaw right.
        """
        yawQuat = Quaternion.setToRotationAboutY( amount )
        self.rotateQuaternion( yawQuat )
    
    def yawRight( self, amount ):
        self.yaw( -amount )
    
    def yawLeft( self, amount ):
        self.yaw( amount )
    
    def roll( self, amount ):
        rollQuat = Quaternion.setToRotationAboutZ( amount )
        self.rotateQuaternion( rollQuat )
    
    def rollRight( self, amount ):
        self.roll( -amount )
    
    def rollLeft( self, amount ):
        self.roll( amount )
        
    def lookAtWorld( self, target, upAxis ):
        self._setDirty()
        raise NotImplementedError(
            "SceneNode.lookAt not implemented for non local translations"
            )
    
    def translate( self, vector ):
        self._translation += vector
        self._setDirty()
    
    def translateForward( self, amount ):
        if amount == 0.0:
            return
        
        matrix = Matrix33.fromInertialToObjectQuaternion( self._orientation )
        forwardVec = Matrix33.inertialToObject( [ 0.0, 0.0, -1.0 ], matrix )
        forwardVec *= amount
        self._translation += forwardVec
        self._setDirty()
    
    def translateBackward( self, amount ):
        self.translateForward( -amount )
    
    def translateRight( self, amount ):
        if amount == 0.0:
            return
        
        matrix = Matrix33.fromInertialToObjectQuaternion( self._orientation )
        rightVec = Matrix33.inertialToObject( [ 1.0, 0.0, 0.0 ], matrix )
        rightVec *= amount
        self._translation += rightVec
        self._setDirty()
    
    def translateLeft( self, amount ):
        self.translateRight( -amount )
    
    def translateUp( self, amount ):
        if amount == 0.0:
            return
        
        matrix = Matrix33.fromInertialToObjectQuaternion( self._orientation )
        upVec = Matrix33.inertialToObject( [ 0.0, 1.0, 0.0 ], matrix )
        upVec *= amount
        self._translation += upVec
        self._setDirty()
    
    def translateDown( self, amount ):
        self.translateUp( -amount )
    
    def setScale( self, scale ):
        self.scale[:] = scale
    
    def addChild( self, node ):
        previousParent = node.parent
        if previousParent != None:
            previousParent.removeChild( node )
        
        # add the node
        self.children.add( node )
        
        # set ourself as the parent
        node._parent = weakref.ref( self )
        
        # mark the node as dirty
        node._setDirty()
    
    def removeChild( self, node ):
        self.children.remove( node )
        node._parent = None
    
    @property
    def parent( self ):
        if self._parent != None:
            return self._parent()
        return None
    
    def onContextLost( self ):
        # we don't need to do anything
        # but our children might
        for child in self.children:
            child.onContextLost()
    
    def applyTranslations( self ):
        # apply our scale
        glScalef( self.scale[ 0 ], self.scale[ 1 ], self.scale[ 2 ] )
        
        # convert our quaternion to a matrix
        matrix = Matrix44.fromInertialToObjectQuaternion( self._orientation )
        
        # add our translation to the matrix
        Matrix44.setTranslation( matrix, self._translation, out = matrix )
        
        # convert to ctype for OpenGL
        glMatrix = (GLfloat * matrix.size)(*matrix.flat) 
        glMultMatrixf( glMatrix )
    
    def render( self ):
        # apply our transforms
        glPushMatrix()
        
        self.applyTranslations()
        
        if self.renderDebugCube == True:
            DebugCube.renderDebugCube()
        
        # continue on to our children
        for child in self.children:
            child.render()
        
        # undo our transforms
        glPopMatrix()
    


if __name__ == "__main__":
    """
    Tree methods
    """
    root = SceneNode()
    
    child1_1 = SceneNode()
    child1_2 = SceneNode()
    
    child2_1 = SceneNode()
    child2_2 = SceneNode()
    
    root.addChild( child1_1 )
    root.addChild( child1_2 )
    
    child1_1.addChild( child2_1 )
    child1_2.addChild( child2_2 )
    
    assert child1_1.parent is root
    assert child1_1 in root.children
    assert child1_2.parent is root
    assert child1_2 in root.children
    
    assert child2_1.parent is child1_1
    assert child2_1 in child1_1.children
    assert child2_2.parent is child1_2
    assert child2_2 in child1_2.children
    
    child1_1.addChild( child2_2 )
    
    assert child2_2.parent is child1_1
    assert child2_2 in child1_1.children
    assert child2_2 not in child1_2.children
    

