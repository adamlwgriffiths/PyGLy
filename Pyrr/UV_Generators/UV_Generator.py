'''
Created on 29/05/2011

@author: adam
'''


class UV_Generator( object ):
    
    
    def __init__( self ):
        super( UV_Generator, self ).__init__()
    
    def generateCoordinates( self, vertices, normal ):
        raise NotImplementedError(
            "Not implemented in base class, instantiate a child class instead"
            )
    
