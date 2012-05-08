'''
Created on 29/02/2012

@author: adam
'''

from pyglet.gl import *

from pygly.dispatcher import Dispatcher


class Digital( Dispatcher ):
    """
    This class provides access to a single digital
    device.

    Most physical hardware device will only require
    a single 'Digital' input object.

    Values provided are the event type
    (pressed / released) and the input (a button).
    """
    
    def __init__( self, device ):
        super( Digital, self ).__init__()
        
        self.device = device
        self.handlers = set()

    def dispatch_event( self, event, value ):
        """
        Sends an event to all registered handler
        functions.
        """
        for handler in self.handlers:
            handler( self.device, event, value )

