"""Provides methods to replace default behaviors.
"""
import pyglet


def patch_idle_loop():
    """Replaces the default Pyglet idle loop.

    By default, pyglet calls on_draw after EVERY batch of events
    which without hooking into, causes ghosting
    and if we do hook into it, it means we render after every event
    which is REALLY REALLY BAD
    http://www.pyglet.org/doc/programming_guide/the_application_event_loop.html
    """
    def idle( self ):
        pyglet.clock.tick( poll = True )
        # don't call on_draw
        return pyglet.clock.get_sleep_time( sleep_idle = True )

    # check that the event loop has been over-ridden
    if pyglet.app.EventLoop.idle != idle:
        # over-ride the default event loop
        pyglet.app.EventLoop.idle = idle

def patch_window_for_opengl_core():
    """Patches out core pyglet functions that use OpenGL legacy.

    The functions 'pyglet.window.BaseWindow.on_resize' and
    'pyglet.window.BaseWindow.draw_mouse_cursor' will be replaced
    with empty stub functions.
    """
    def on_resize( self, width, height ):
        # don't do anything
        pass

    def draw_mouse_cursor( self ):
        # don't do anything
        pass

    # patch out any pyglet functions using
    # opengl legacy calls
    pyglet.window.BaseWindow.on_resize = on_resize
    pyglet.window.BaseWindow.draw_mouse_cursor = draw_mouse_cursor
