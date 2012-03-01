'''
Created on 01/03/2012

@author: adam
'''

from pyglet.gl import *


class Dispatcher( object ):
    """
    """
    
    def __init__( self ):
        super( Dispatcher, self ).__init__()
        
        self.handlers = set()

    def register_handler( self, handler ):
        """
        Adds a handler to the list of
        handlers to receive events.

        @param handler: Must be a callable function.
        Function must take the parameters:
            device, axis, value
        """
        assert handler not in self.handlers
        assert callable( handler )

        self.handlers.add( handler )
    
    def unregister_handler( self, handler ):
        """
        Removes a registered handler so it
        no longer receives updates.

        @param handler: Must be a callable function.
        Function must take the parameters:
            device, axis, value

        @raise KeyError: if not present.
        """
        self.handlers.remove( handler )


if __name__ == "__main__":
    obj = Dispatcher()

    def handler():
        pass

    assert handler not in obj.handlers
    obj.register_handler( handler )

    assert handler in obj.handlers

    obj.unregister_handler( handler )
    assert handler not in obj.handlers

