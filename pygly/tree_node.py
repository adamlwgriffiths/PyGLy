'''
Created on 11/05/2012

@author: adam
'''

import weakref
from collections import deque

    
class TreeNode( object ):
    """
    Base class for Tree branch objects.

    Supports a single parent and N children.
    """
    
    def __init__( self ):
        super( TreeNode, self ).__init__()
        
        self._parent = None
        self.children = set()
    
    def add_child( self, node ):
        """
        Attaches a child to the node.

        @raise ValueError: Raised if the child
        already has a parent.
        """
        if node.parent != None:
            raise ValueError( "Node has an existing parent" )
        
        # add the node
        self.children.add( node )
        
        # set ourself as the parent
        node._parent = weakref.ref( self )
    
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

    def dfs( self ):
        queue = deque( list(self.children) )
        while queue:
            node = queue.pop()
            if hasattr( node, 'children' ):
                queue.extend( list(node.children) )
            yield node

    def bfs( self ):
        queue = deque( list(self.children) )
        while queue:
            node = queue.pop()
            if hasattr( node, 'children' ):
                queue.extendleft( list(node.children) )
            yield node

    def predecessors( self ):
        parent = self.parent
        while parent != None:
            yield parent
            parent = parent.parent

