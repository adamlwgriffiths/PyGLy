# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 13:21:48 2011

@author: adam
"""


class Material( object ):
    
    def __init__( self, name ):
        super( Material, self ).__init__()
        
        self.name = name
        
        self.texture0 = None
        self.texture1 = None
        self.texture2 = None
        self.texture3 = None
        self.texture4 = None
        self.texture5 = None
        self.texture6 = None
        self.texture7 = None
    
    def bind():
        # apply_material
        # http://assimp.svn.sourceforge.net/viewvc/assimp/trunk/samples/SimpleOpenGL/Sample_SimpleOpenGL.c?revision=973&view=markup
        pass
    
    def unbind():
        pass
    
