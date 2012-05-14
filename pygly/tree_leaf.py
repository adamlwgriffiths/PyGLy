'''
Created on 11/05/2012

@author: adam
'''

import weakref

    
class TreeLeaf( object ):
    """
    Base class for Tree Leaf objects.

    Supports a single parent.
    Cannot have children.
    """
    
    def __init__( self ):
        super( TreeLeaf, self ).__init__()
        
        self._parent = None
    
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

    def predecessors( self ):
        parent = self.parent
        while parent != None:
            yield parent
            parent = parent.parent

