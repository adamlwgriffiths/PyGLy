'''
Created on 29/02/2012

@author: adam
'''

from pyglet.gl import *

from pygly.dispatcher import Dispatcher


class Analog( Dispatcher ):
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
        self.handlers = set()
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
            (absolute, relative)
            )
    
    def clear_delta( self ):
        """
        Sets the stored relative value to 0.
        This should probably be called at the
        end of each frame.
        """
        self.delta = 0

    def dispatch_event( self, value ):
        """
        Sends an event to all registered handler
        functions.
        """
        for handler in self.handlers:
            handler( self.device, self.axis, value )
    

if __name__ == "__main__":
    device = Analog( 'mouse', 'x' )

    def handle_event( device, event, value ):
        print '[%s] %s: %s' % (device, event, value)

    assert handle_event not in device.handlers
    device.register_handler( handle_event )
    device.dispatch_event( (100, 5)  )
    assert handle_event in device.handlers
    device.unregister_handler( handle_event )
    assert handle_event not in device.handlers


