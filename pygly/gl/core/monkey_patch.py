"""Provides OpenGL Core functions.
"""

import pyglet.window

def _on_resize( self, width, height ):
    # don't do anything
    pass

def _draw_mouse_cursor( self ):
    # don't do anything
    pass

def patch_window():
    # patch out any pyglet functions using
    # opengl legacy calls
    pyglet.window.BaseWindow.on_resize = _on_resize
    pyglet.window.BaseWindow.draw_mouse_cursor = _draw_mouse_cursor

