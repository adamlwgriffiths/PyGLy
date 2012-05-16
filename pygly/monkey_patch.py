'''
Created on 20/06/2011

@author: adam
'''

from pyglet.gl import *


def idle( self ):
    """
    We need to over-ride the default idle logic.

    By default, pyglet calls on_draw after EVERY batch of events
    which without hooking into, causes ghosting
    and if we do hook into it, it means we render after every event
    which is REALLY REALLY BAD
    http://www.pyglet.org/doc/programming_guide/the_application_event_loop.html
    """
    pyglet.clock.tick( poll = True )
    # don't call on_draw
    return pyglet.clock.get_sleep_time( sleep_idle = True )

def patch_idle_loop():
    # check that the event loop has been over-ridden
    if pyglet.app.EventLoop.idle != idle:
        # over-ride the default event loop
        pyglet.app.EventLoop.idle = idle

