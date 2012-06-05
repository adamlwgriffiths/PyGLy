'''
Created on 29/02/2012

@author: adam
'''

import sys

from pyglet.gl import *
from pyglet.event import EventDispatcher


class Digital( EventDispatcher ):
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

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_digital_input( digital, event, value ):
            '''A digital input has been triggered.

            :event:
            '''

# register our custom events
Digital.register_event_type( 'on_digital_input' )

