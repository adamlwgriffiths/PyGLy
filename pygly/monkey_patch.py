'''Provides methods to replace default behaviors.

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

from pyglet.gl import *


def idle( self ):
    """An alternate idle loop than Pyglet's default.

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
    """Replaces the default Pyglet idle look with the :py:func:`idle` function in this module.
    """
    # check that the event loop has been over-ridden
    if pyglet.app.EventLoop.idle != idle:
        # over-ride the default event loop
        pyglet.app.EventLoop.idle = idle

