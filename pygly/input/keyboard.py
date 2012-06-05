'''
Created on 24/06/2011

@author: adam
'''

from pyglet.gl import *
import pyglet.window.key

from digital import Digital


class Keyboard( object ):
    # allow access to pyglet.window.key
    keys = pyglet.window.key
    down = 'down'
    up = 'up'
    
    def __init__( self, window, name = 'keyboard' ):
        super( Keyboard, self ).__init__()
        
        self.name = name
        self.window = window
        self.key_state = pyglet.window.key.KeyStateHandler()
        self.digital = Digital( self.name )
    
        self.window.push_handlers(
            self.key_state
            )
        self.window.push_handlers(
            on_key_press = self.on_key_press,
            on_key_release = self.on_key_release
            )
    
    def __del__( self ):
        if self.window != None:
            self.window.remove_handlers(
                self.on_key_press,
                self.on_key_release,
                self.key_state
                )
    
    def is_key_down( self, key ):
        return self.key_state[ key ]
    
    def __getitem__( self, k ):
        # Handles [] operator
        # redirect to our keyboard handler
        return self.key_state[ k ]
    
    def on_key_press( self, symbol, modifiers ):
        """
        Pyglet event handler method.

        Notifies and handlers of the event via their
        'on_key_press' method.
        Do NOT rename this function.
        """
        self.digital.dispatch_event(
            'on_digital_input',
            self.digital,
            Keyboard.down,
            (symbol, modifiers)
            )
    
    def on_key_release( self, symbol, modifiers ):
        """
        Pyglet event handler method.

        Notifies and handlers of the event via their
        'on_key_release' method.
        Do NOT rename this function.
        """
        self.digital.dispatch_event(
            'on_digital_input',
            self.digital,
            Keyboard.up,
            (symbol, modifiers)
            )


if __name__ == "__main__":
    from pyglet.gl import *
    
    window = pyglet.window.Window( fullscreen = False )
    
    keyboard = Keyboard( window )
    
    def handler( digital, event, value ):
        print '[%s] %s: (%s, %s)' % (
            digital.device,
            event,
            value[ 0 ],
            value[ 1 ]
            )

        #global window
        #window.close()

    def watcher( dt ):
        global keyboard
        if keyboard[ keyboard.keys.SPACE ]:
            print 'SPACE is down'
            global window
            window.close()

    keyboard.digital.push_handlers(
        on_digital_input = handler
        )
    pyglet.clock.schedule_interval( watcher, (1.0 / 60.0) )

    pyglet.app.run()
    
    

