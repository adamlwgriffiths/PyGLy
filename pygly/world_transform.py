'''
Created on 11/06/2012

@author: adam
'''

import sys

import numpy
from pydispatch import dispatcher

from pyrr import quaternion
from pyrr import matrix33
from pyrr import matrix44

from object_space import ObjectSpace
from inertial_space import InertialSpace
from tree_node import TreeNode
from transform import Transform


class WorldTransform( TreeNode ):


    def __init__( self, transform ):
        super( WorldTransform, self ).__init__()

        self.set_dirty()

        # the local transform
        self._transform = transform

        # register our event handlers
        # listen for transform changes from local transform
        dispatcher.connect(
            self._on_transform_changed,
            Transform.on_transform_changed,
            self._transform
            )

        # listen for new parents and children
        dispatcher.connect(
            self._on_parent_changed,
            TreeNode.on_parent_changed,
            self
            )

    def set_dirty( self ):
        self._orientation = None
        self._translation = None
        self._scale = None
        self._matrix = None

    def _on_parent_changed( self, old_parent, new_parent ):
        # mark ourself as dirty
        self.set_dirty()

        # unregister from our old parent's events
        if old_parent != None:
            dispatcher.disconnect(
                self._on_transform_changed,
                Transform.on_transform_changed,
                old_parent
                )

        # register to our new parent's events
        if new_parent != None:
            dispatcher.connect(
                self._on_transform_changed,
                Transform.on_transform_changed,
                new_parent
                )


    def _on_transform_changed( self ):
        """
        .. note::
            Changing this value will dispatch an
            'on_transform_changed' event.
        """
        # mark ourself as dirty
        self.set_dirty()

        # notify others of our change
        dispatcher.send( Transform.on_transform_changed, self )

    @property
    def object( self ):
        return ObjectSpace( self )

    @property
    def inertial( self ):
        return InertialSpace( self )
    
    @property
    def scale( self ):
        if self._scale == None:
            if self.parent == None:
                # we don't have a parent
                # so just use our current local scale
                self._scale = self._transform.scale.copy()
            else:
                # apply our parents scale to our local scale
                self._scale = self._transform.scale * self.parent.scale

        return self._scale

    @scale.setter
    def scale( self, scale ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed

        # determine the correct scale to
        # modify our parents to make our scale
        # == to the passed in value
        self._transform.scale = scale / self.parent.scale

    @property
    def orientation( self ):
        if self._orientation == None:
            if self.parent == None:
                # we don't have a parent
                # so just use our current local orientation
                self._orientation = self._transform.orientation.copy()
            else:
                # multiply our rotation by our parents
                # order is important, our quaternion should
                # be the second parameter
                self._orientation = quaternion.cross(
                    self.parent.orientation,
                    self._transform.orientation
                    )
                # ensure the quaternion is normalised
                self._orientation = quaternion.normalise( self._orientation )

        return self._orientation

    @orientation.setter
    def orientation( self, quaternion ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed
        raise NotImplementedError

    @property
    def translation( self ):
        if self._translation == None:
            if self.parent == None:
                # we don't have a parent
                # so just use our current local translation
                self._translation = self._transform.translation.copy()
            else:
                # rotate our translation by our parent's
                # world orientation
                # this will include our parent's world translation
                self._translation = matrix44.apply_to_vector(
                    self.parent.matrix,
                    self._transform.translation
                    )

        return self._translation

    @translation.setter
    def translation( self, translation ):
        # don't check if the value hasn't changed
        # using -= or += will cause this to fail
        # due to python calling, getter, obj +, setter
        # which would look as if the value hasn't changed
        raise NotImplementedError

    @property
    def matrix( self ):
        """
        Returns a matrix representing the node's
        object translation, orientation and
        scale.
        """
        if self._matrix == None:
            if self.parent == None:
                self._matrix = self._transform.matrix.copy()
            else:
                self._matrix = matrix44.multiply(
                    self._transform.matrix,
                    self.parent.matrix
                    )

        return self._matrix

