"""Provides OpenGL legacy functions.
"""

from contextlib import contextmanager

from pyglet.gl import *
import numpy


@contextmanager
def begin( mode ):
    """Wraps glBegin and glEnd in a
    context manager, providing the 'with'
    keyword.

    For example:
    with begin( GL_TRIANGLES ):
        glVertex2f( 0.0, 0.0 )
        glVertex2f( 0.5, 1.0 )
        glVertex2f( 1.0, 0.0 )
    """
    glBegin( mode )
    yield
    glEnd()

@contextmanager
def matrix_mode( mode ):
    """Wraps glMatrixMode in a context manager,
    providing the 'with' keyword.
    Automatically restores the existing matrix
    mode on exit.

    For example:
    with matrix_mode( GL_MODELVIEW ):
        pass
    """
    glPushAttrib( GL_MATRIX_MODE )
    glMatrixMode( mode )
    yield
    glPopAttrib()

@contextmanager
def load_matrix( mat ):
    """Wraps glPushMatrix, glPopMatrix and
    glLoadMatrixf in a context manager,
    providing the 'with' keyword.

    Arrays will be loaded as 32-bit floats.

    For example:
    with load_matrix( world_matrix ):
        pass
    """
    glPushMatrix()
    m = mat

    # check if the matrix is a numpy array or
    if isinstance( mat, numpy.ndarray ):
        # ensure we use float32s
        m = mat.astype('float32').flat

    glLoadMatrixf( (GLfloat * len(m))(*m) )
    yield
    glPopMatrix()

