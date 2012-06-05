'''
Created on 28/06/2011

@author: adam
'''

import numpy
from pyglet.gl import *
import pyglet.window.mouse

from analog import Analog


class Mouse( object ):
    x = 0
    y = 1

    # allow access to pyglet.window.mouse
    buttons = pyglet.window.mouse
    
    def __init__( self, window, name = 'mouse' ):
        super( Mouse, self ).__init__()

        self.name = name
        self.window = window
        
        self.axis = [
            Analog( self.name, 'x' ),
            Analog( self.name, 'y' )
            ]
        self.window.push_handlers(
            on_mouse_motion = self.on_mouse_motion
            )

    def __del__( self ):
        if self.window != None:
            self.window.remove_handlers( self, self )
    
    def on_mouse_motion( self, x, y, dx, dy ):
        self.axis[ Mouse.x ].value_changed( x, dx )
        self.axis[ Mouse.y ].value_changed( y, dy )

    def clear_delta( self ):
        for axis in self.axis:
            axis.clear_delta()

    def axis_x( self ):
        return self.axis[ Mouse.x ]

    def axis_y( self ):
        return self.axis[ Mouse.y ]

    @property
    def absolute_position( self ):
        return [
            self.axis[ Mouse.x ].value,
            self.axis[ Mouse.y ].value
            ]

    @property
    def relative_position( self ):
        return [
            self.axis[ Mouse.x ].delta,
            self.axis[ Mouse.y ].delta
            ]


if __name__ == '__main__':
    from pyglet.gl import *

    window = pyglet.window.Window( fullscreen = False )
    mouse = Mouse( window )

    """
    def update( dt ):
        global mouse
        print mouse.absolute_position

        global window
        window.close()

    pyglet.clock.schedule_interval( update, (1.0 / 60.0) )
    """
    def update( analog, value ):
        global mouse
        print "[%s] %s: absolute: %f relative: %f" % (
            analog.device,
            analog.axis,
            value[ 0 ],
            value[ 1 ]
            )

        window.close()

    mouse.axis_x().push_handlers( on_analog_input = update )
    pyglet.app.run()

