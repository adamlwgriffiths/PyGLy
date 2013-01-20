"""Window management functions.
"""
from pyrr import rectangle


def create_rectangle( window ):
    """Creates a rectangle object representing the window
    size in pixels.
    The rectangle is in the format of Pyrr.rectangle.

    Returns:
        The size of the window in pixels represented as a
        NumPy array with shape (2,2).
    """
    return rectangle.create_from_position(
        x = 0,
        y = 0,
        width = window.width,
        height = window.height
        )
