'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import sys
import weakref
from collections import deque

from pyglet.event import EventDispatcher

    
class TreeNode( EventDispatcher ):
    """Base class for Tree branch objects.

    Supports a single parent.
    Can have 0-N children.
    """
    
    def __init__( self ):
        """Creates a tree node object.
        """
        super( TreeNode, self ).__init__()
        
        self._parent = None
        self._children = set()
    
    def add_child( self, node ):
        """Attaches a child to the node.

        .. note:: Dispatches an 'on_child_added' event.

        Raises:
            ValueError: Raised if the child
            already has a parent.
        """
        if node.parent != None:
            raise ValueError( "Node has an existing parent" )
        
        # add the node
        self._children.add( node )
        
        # set ourself as the parent
        node.parent = self

        # notify others of our change
        self.dispatch_event(
            'on_child_added',
            node
            )
    
    def remove_child( self, node ):
        """Removes a child from the node.

        .. note:: Dispatches an 'on_child_removed' event.

        Raises:
            KeyError: Raised if the node
            is not a child of the node.
        """
        # remove from our list of children
        self._children.remove( node )

        # unset the node's parent
        node.parent = None

        # notify others of our change
        self.dispatch_event(
            'on_child_removed',
            node
            )

    @property
    def children( self ):
        return self._children
    
    @property
    def parent( self ):
        """The parent of the node or None if there isn't one.

        The parent value should **not** be changed manually.
        Instead use the 'remove_child' method on the parent.

        .. note::
            When the parent value is changed, the 'on_parent_changed'
            event will be dispatched.

        .. note ::
            This is an @property decorated method which allows
            retrieval and assignment of the scale value.

        Raises:
            ValueError: Raised is the node already has a parent.
            ValueError: Raised if the node is not a child of the
            new parent. This is handled internally.
        """
        if self._parent != None:
            return self._parent()
        return None

    @parent.setter
    def parent( self, parent ):
        """Sets the parent of the node.
        This should not be called manually.

        Raises:
            ValueError: Raised if the node already has a
            parent or if the node is not a child of the
            new parent.
        """
        if self.parent != None:
            raise ValueError( "Node has an existing parent" )
        if self not in parent.children:
            raise ValueError( "Node not child of parent" )

        old_parent = self.parent
        self._parent = weakref.ref( parent )

        # notify others of our change
        self.dispatch_event(
            'on_parent_changed',
            old_parent,
            self.parent
            )

    def dfs( self ):
        queue = deque( list(self._children) )
        while queue:
            node = queue.pop()
            if hasattr( node, 'children' ):
                queue.extend( list(node._children) )
            yield node

    def bfs( self ):
        queue = deque( list(self._children) )
        while queue:
            node = queue.pop()
            if hasattr( node, 'children' ):
                queue.extendleft( list(node._children) )
            yield node

    def predecessors( self ):
        parent = self.parent
        while parent != None:
            yield parent
            parent = parent.parent

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_parent_changed( old_parent, new_parent ):
            '''A parent was set.

            :event:
            '''

        def on_child_added( child ):
            '''A child was added

            :event:
            '''

        def on_child_removed( child ):
            '''A child was removed

            :event:
            '''

TreeNode.register_event_type( 'on_parent_changed' )
TreeNode.register_event_type( 'on_child_added' )
TreeNode.register_event_type( 'on_child_removed' )

