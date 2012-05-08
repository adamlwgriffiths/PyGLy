# -*- coding: utf-8 -*-
"""
Created on 24/03/2012

http://www.martinreddy.net/gfx/3d/OBJ.spec
http://en.wikipedia.org/wiki/Wavefront_.obj_file
http://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Load_OBJ
http://openglsamples.sourceforge.net/files/glut_obj.cpp

TODO: implement as much of the spec as makes sense http://www.martinreddy.net/gfx/3d/OBJ.spec
TODO: smoothing groups
TODO: colour
TODO: materials
TODO: points
TODO: curved surfaces (just render as flat surface)
TODO: lines

@author: adam
"""

from pyglet.gl import *



class OBJ_Mesh( object ):
    
    def __init__( self, filename ):
        super( OBJ_Mesh, self ).__init__()
        
        self.filename = filename
        self.display_list = None
    
    def load( self ):
        # open the file in ascii mode
        with open( self.filename, 'r' ) as f:
            self.load_data( f )
    def load_data( self, data ):
        self.display_list = glGenLists( 1 )
        glNewList( self.display_list, GL_COMPILE )

        vertices = []
        tcs = []
        normals = []

        def process_line( line ):
            # remove whitespace
            line = line.lstrip()

            # check for comments and ignore them
            if line.startswith( '#' ):
                # comment
                return

            # tokenize the line
            tokens = line.split()

            # ensure the line isn't empty
            if len(tokens) <= 0:
                return

            if tokens[ 0 ] == 'v':
                # vertex
                # v x y z w
                # w is optional, default is 1.0
                # we ignore w
                if ( len( tokens ) < 4 or len( tokens ) > 5 ):
                    raise ValueError( "Vertex entry contains an invalid number of values" )
                vertices.append(
                    (
                        float(tokens[ 1 ]),
                        float(tokens[ 2 ]),
                        float(tokens[ 3 ])
                        )
                    )
            elif tokens[ 0 ] == 'vt':
                # texture coords
                # vt tu tv [tw]
                # tv is optional, default is 0.0
                # w is optional, default is 0.0
                # we ignore w
                if ( len( tokens ) < 2 or len( tokens ) > 4 ):
                    raise ValueError( "Texture Coordinate entry contains an invalid number of values" )
                tcs.append(
                    (
                        float(tokens[ 1 ]),
                        float(tokens[ 2 ]) if len( tokens >= 2 ) else 0.0
                        )
                    )
            elif tokens[ 0 ] == 'vn':
                # vertex normals
                # vn x y z
                if ( len( tokens ) != 3 ):
                    raise ValueError( "Vertex normal entry contains an invalid number of values" )
                normals.append(
                    (
                        float(tokens[ 1 ]),
                        float(tokens[ 2 ]),
                        float(tokens[ 3 ])
                        )
                    )
            elif tokens[ 0 ] == 'f':
                # face
                # f v1 v2 v3 ...
                # f v1/vt1 v2/vt2 v3/vt3 ...
                # f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3 ...
                # f v1//vn1 v2//vn2 v3//vn3 ...
                # face type depends on the number of vertices

                # ignore the first token
                faces = tokens[1:]
                numVertices = len(faces)

                # use triangle fans
                # this handles the case of
                # 3 vertices (triangles)
                # 4 vertices (quads)
                # >4 vertices (fan)
                glBegin( GL_TRIANGLE_FAN )

                # for each entry we need to extract the data
                # data is delemited by /'s
                for entry in faces:
                    # tokenize each entry
                    entries = entry.split('/')

                    # we must do the vertex last
                    # or the normal and tc will apply
                    # to the next vertex

                    if len( entries ) >= 2 and entries[ 1 ] != '':
                        # vt
                        # convert to int and subtract 1
                        # as the values are 1 indexed, not 0
                        index = int(entries[ 1 ])
                        # account for relative indices
                        if ( index < 0 ):
                            index = len( tcs ) + index
                        else:
                            index -= 1

                        glTexCoord2f(
                            tcs[ index ][ 0 ],
                            tcs[ index ][ 1 ]
                            )
                    if len( entries ) >= 3 and entries[ 2 ] != '':
                        # vn
                        # convert to int and subtract 1
                        # as the values are 1 indexed, not 0
                        index = int(entries[ 2 ]) 
                        if ( index < 0 ):
                            index = len( normals ) + index
                        else:
                            index -= 1

                        glNormal3f(
                            normals[ index ][ 0 ],
                            normals[ index ][ 1 ],
                            normals[ index ][ 2 ]
                            )
                    # v
                    # convert to int and subtract 1
                    # as the values are 1 indexed, not 0
                    index = int(entries[ 0 ])
                    if ( index < 0 ):
                        index = len( vertices ) + index
                    else:
                        index -= 1

                    glVertex3f(
                        vertices[ index ][ 0 ],
                        vertices[ index ][ 1 ],
                        vertices[ index ][ 2 ]
                        )
                # end the current primitive
                glEnd()


        # process each line of our input
        for line in data:
            process_line( line )

        glEndList()

    def render( self ):
        glCallList( self.display_list )

