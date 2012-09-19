"""Provides OpenGL Core functions.
"""

import pyglet.window

def _on_resize( self, width, height ):
    # don't bloody well do anything
    pass

def _draw_mouse_cursor( self ):
    pass

def _draw( self ):
    pass

def patch_window():
    pyglet.window.BaseWindow.on_resize = _on_resize
    pyglet.window.BaseWindow.draw_mouse_cursor = _draw_mouse_cursor
    pyglet.window.BaseWindow.draw = _draw

