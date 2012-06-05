'''
Created on 29/02/2012

@author: adam
'''

import sys

from pyglet.gl import *
from pyglet.event import EventDispatcher


class Analog( EventDispatcher ):
    """
    This class provides access to a single analog
    input.

    A physical hardware device may be composed of
    multiple analog inputs.
    For example, a mouse has 2: x and y.

    Values provided are the absolute value of the
    axis and the change in value since the last
    call to 'clear_delta()'.
    """
    
    def __init__( self, device, axis ):
        super( Analog, self ).__init__()
        
        self.device = device
        self.axis = axis
        self.value = 0
        self.delta = 0

    def value_changed( self, absolute, relative ):
        """
        Updates the analog values.

        Automatically offsets the current delta
        value by the new relative value.

        To clear the delta, call 'clear_delta()'.
        """
        self.value = absolute
        # add the delta value
        self.delta += relative

        self.dispatch_event(
            'on_analog_input',
            self,
            (absolute, relative)
            )
    
    def clear_delta( self ):
        """
        Sets the stored relative value to 0.
        This should probably be called at the
        end of each frame.
        """
        self.delta = 0

    # document our events
    if hasattr( sys, 'is_epydoc' ):
        def on_analog_input( analog, value ):
            '''An analog input has been triggered.

            :event:
            '''

# register our custom events
Analog.register_event_type( 'on_analog_input' )

