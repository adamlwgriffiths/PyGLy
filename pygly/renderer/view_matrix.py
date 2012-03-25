'''
Created on 20/06/2011

@author: adam
'''

import weakref

from pyglet.gl import *

class ViewMatrix( object ):


    def __init__( self ):
        super( ViewMatrix, self ).__init__()

    def push_view_matrix( self, viewport ):
        pass

    def pop_view_matrix( self ):
        pass

