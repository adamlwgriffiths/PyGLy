'''
.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import weakref

    
class TreeLeaf( object ):
    """Base class for Tree Leaf objects.

    Supports a single parent.
    Cannot have children.
    """
    
    def __init__( self ):
        """Creates a tree leaf object.
        """
        super( TreeLeaf, self ).__init__()
        
        self._parent = None
    
    @property
    def parent( self ):
        """The current parent of the node or None
        if there isn't one.

        This is an @property decorated method which allows
        retrieval and assignment of the scale value.
        """
        if self._parent != None:
            return self._parent()
        return None

    def predecessors( self ):
        """Returns successive parents of the node.

        Generator function that allows iteration
        up the tree.
        """
        parent = self.parent
        while parent != None:
            yield parent
            parent = parent.parent

