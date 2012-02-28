'''
Created on 20/06/2011

@author: adam
'''

import weakref


class WeakRef( object ):
    
    
    def __init__(self, object = None ):
        super( WeakRef , self).__init__()
        
        self.object = None
        if object != None:
            self.object = weakref.ref( object )
    
    def setObject( self, object ):
        self.object = weakref.ref( object )
    
    def __call__(self):
        """Return a pair containing the referent and the number of
        times the reference has been called.
        """
        if self.object == None:
            return None
        
        object = self.object()
        return object
    


