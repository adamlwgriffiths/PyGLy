# -*- coding: utf-8 -*-
"""
Uses the Open Asset Importer module to load meshes.
http://assimp.sourceforge.net/

Created on Wed Sep 14 17:18:48 2011

@author: adam
"""

from ctypes import *
import os.path

from pyglet.gl import *

# we need to add the location of the dll to the
# list of search directories
# TODO: change this to use resource locations
# http://www.pyglet.org/doc/programming_guide/loading_resources.html
from pyassimp import helper
helper.additional_dirs.append(
    r'C:\Users\adam\workspace\PyGLy\contrib\assimp--2.0.863-sdk\bin\assimp_release-dll_win32'
    )

from pyassimp import pyassimp, structs

TextureLayer = [
    GL_TEXTURE0,
    GL_TEXTURE1,
    GL_TEXTURE2,
    GL_TEXTURE3
    ]

Diffuse     = [ 0.8, 0.8, 0.8, 1.0 ]
Specular    = [ 0.0, 0.0, 0.0, 1.0 ]
Ambient     = [ 0.2, 0.2, 0.2, 1.0 ]
Emission    = [ 0.0, 0.0, 0.0, 1.0 ]

MaterialKeys = {
    "name" : "?mat.name",
    "texture" : "$tex.file",
    
    "specular" : "$clr.specular",
    "ambient" : "$clr.ambient",
    "diffuse" : "$clr.diffuse",
    "emissive" : "$clr.emissive",
    
    "bumpmap_scale" : "$mat.bumpscaling",
    "shininess" : "$mat.shininess",
    "shine_percent" : "$mat.sinpercent",
    "opacity" : "$mat.opacity",
    "two_sided" : "$mat.twosided",
    
    "blend_mode" : "$tex.blend",
    # "$tex.uvtrafo"
    # "$tex.mapmodev",
    # "$tex.mapmodeu",
    }

class OAI_Mesh( object ):
    # TODO: merge texture and material pre-loading
    # TODO: add lights
    # TODO: add camera
    
    def __init__( self, filename ):
        super( OAI_Mesh, self ).__init__()
        
        self.filename = filename
        self._frame = 0
        self.displayList = None
        self.images = {}
    
    def load( self ):
        scene = pyassimp.load( self.filename )
        
        # drop the existing materials
        # TODO: drop the existing materials
        
        # load the materials
        self.load_textures( scene )
        
        # clear the existing display lists
        self.displayList = None
        
        self.displayList = glGenLists( 1 )
        glNewList( self.displayList, GL_COMPILE )
        
        glEnable( GL_TEXTURE_2D )
        
        # render the meshes
        self.recursive_render( scene, scene.mRootNode.contents )
        
        glEndList()
        
        # release the model
        pyassimp.release(scene)
    
    def load_textures( self, scene ):
        # textures should be loaded into a key, value store
        # to avoid loading the same texture multiple times
        # http://assimp.svn.sourceforge.net/viewvc/assimp/trunk/samples/SimpleTexturedOpenGL/SimpleTexturedOpenGL/src/model_loading.cpp?revision=1084&view=markup
        
        images = {}
        for material in scene.materials:
            properties = pyassimp.GetMaterialProperties( material )
            
            if MaterialKeys[ 'texture' ] in properties:
                filename = properties[ MaterialKeys[ 'texture' ] ]
                if filename not in self.images:
                    try:
                        absFilename = "%s/%s" % (
                            os.path.dirname( self.filename ),
                            filename
                            )
                        print absFilename
                        image = pyglet.image.load( absFilename )
                        images[ filename ] = image
                    except:
                        print "Exception loading texture %s" % filename
        
        
        # get the number of textures
        textureIds = [ 0 for i in xrange( len(images) ) ]
        c_textureIds = ( GLuint * len(images) )(*textureIds)
        glGenTextures( len(images), c_textureIds )
        textureIds = [ int(i) for i in c_textureIds ]
        
        
        ###################################        
        
        #for material in scene.materials:
        #    self.load_texture( material )
    
    def load_texture( self, material ):   
        properties = pyassimp.GetMaterialProperties( material )
        
        if MaterialKeys[ 'texture' ] in properties:
            filename = properties[ MaterialKeys[ 'texture' ] ]
            if filename not in self.images:
                try:
                    absFilename = "%s/%s" % (
                        os.path.dirname( self.filename ),
                        filename
                        )
                    print absFilename
                    image = pyglet.image.load( absFilename )
                    texture = image.get_texture( rectangle = False )
                    self.images[ filename ] = (image, texture)
                except:
                    print "Exception loading texture"
    
    def apply_material( self, material ):
        properties = pyassimp.GetMaterialProperties( material )
        # FIXME:
        # Materials are done in a stack
        # http://assimp.sourceforge.net/lib_html/materials.html
        # http://assimp.svn.sourceforge.net/viewvc/assimp/trunk/samples/SimpleTexturedOpenGL/SimpleTexturedOpenGL/src/model_loading.cpp?revision=1084&view=markup
        
        
        # check for a texture
        if MaterialKeys[ 'texture' ] in properties:
            filename = properties[ MaterialKeys[ 'texture' ] ]
            if filename in self.images:
                texture = self.images[ filename ][ 1 ]
                #glActiveTexture( GL_TEXTURE0 )
                glBindTexture( GL_TEXTURE_2D, texture.id )
        
        # diffuse
        if MaterialKeys[ 'diffuse' ] in properties:
            diffuse = properties[ MaterialKeys[ 'diffuse' ] ]
        else:
            diffuse = Diffuse
        
        glDiffuse = (GLfloat * 4)(*diffuse)
        glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, glDiffuse )
        
        # specular
        if MaterialKeys[ 'specular' ] in properties:
            specular = properties[ MaterialKeys[ 'specular' ] ]
        else:
            specular = Specular
        
        glSpecular = (GLfloat * 4)(*specular)
        glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, glSpecular )
        
        # ambient
        if MaterialKeys[ 'ambient' ] in properties:
            ambient = properties[ MaterialKeys[ 'ambient' ] ]
        else:
            ambient = Ambient
        
        glAmbient = (GLfloat * 4)(*ambient)
        glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, glAmbient )
        
        # emission
        if MaterialKeys[ 'emissive' ] in properties:
            emission = properties[ MaterialKeys[ 'emissive' ] ]
        else:
            emission = Emission
        
        glEmission = (GLfloat * 4)(*emission)
        glMaterialfv( GL_FRONT_AND_BACK, GL_EMISSION, glEmission )
    
    def recursive_render( self, scene, node ):
        # recursive_render
        # http://assimp.svn.sourceforge.net/viewvc/assimp/trunk/samples/SimpleOpenGL/Sample_SimpleOpenGL.c?revision=973&view=markup
        
        glPushMatrix()
        
        # get the node's transformation
        matrix = node.mTransformation
        
        # convert our matrix from properties to a python list
        matValues = [
            matrix.a1,  matrix.b1,  matrix.c1,  matrix.d1,
            matrix.a2,  matrix.b2,  matrix.c2,  matrix.d2,
            matrix.a3,  matrix.b3,  matrix.c3,  matrix.d3,
            matrix.a4,  matrix.b4,  matrix.c4,  matrix.d4,
            ]
        
        # convert to a glmatrix and push it on the matrix stack
        glMatrix = ( GLfloat * 16 )( *matValues )
        glMultMatrixf( glMatrix )
        
        # iterate through each mesh in the node
        for meshIndex in xrange( node.mNumMeshes ):
            mesh = scene.mMeshes[ node.mMeshes[ meshIndex ] ].contents
            
            # apply material
            self.apply_material( scene.materials[ mesh.mMaterialIndex ] )
            
            # enable / disable lighting based on normals
            if bool( mesh.mNormals[ 0 ] ) == True:
                glEnable( GL_LIGHTING )
            else:
                glDisable( GL_LIGHTING )
            
            if bool( mesh.mColors[ 0 ] ) == True:
                glEnable( GL_COLOR_MATERIAL )
            else:
                glDisable( GL_COLOR_MATERIAL )
            
            # iterate through each face in the mesh
            for faceIndex in xrange( mesh.mNumFaces ):
                face = mesh.mFaces[ faceIndex ]
                
                # determine the type of face we're going to draw
                if face.mNumIndices == 1:
                    faceType = GL_POINTS
                elif face.mNumIndices == 2:
                    faceType = GL_LINES
                elif face.mNumIndices == 3:
                    faceType = GL_TRIANGLES
                else:
                    faceType = GL_POLYGON
                
                glBegin( faceType )
                
                # iterate through each of the vertices in the face
                for indiceIndex in xrange( face.mNumIndices ):
                    index = face.mIndices[ indiceIndex ]
                    
                    # assign the vertex colour
                    # a null pointer indicates there are no colours
                    # null pointers are detected by converting to a boolean
                    if bool(mesh.mColors[ 0 ]) == True:
                        colour = mesh.mColors[ index ]
                        colour = colour.contents
                        glColor4f( colour.r, colour.g, colour.b, colour.a )
                    
                    # assign the texture coordinates
                    """
                    for layer in xrange( len(mesh.mTextureCoords) ):
                        if bool( mesh.mTextureCoords[ layer ] ) == True:
                            texcoords = mesh.mTextureCoords[ layer ]
                            glMultiTexCoord2f(
                                TextureLayer[ layer ],
                                texcoords[ index ].x,
                                1.0 - texcoords[ index ].y
                                )
                    """
                    if bool( mesh.mTextureCoords[ 0 ] ) == True:
                        texcoords = mesh.mTextureCoords[ 0 ]
                        glTexCoord2f(
                            texcoords[ index ].x,
                            texcoords[ index ].y
                            )
                    
                    # assign the vertex normal
                    if bool( mesh.mNormals[ 0 ] ) == True:
                        normal = mesh.mNormals[ index ]
                        glNormal3f( normal.x, normal.y, normal.z )
                    
                    # send the vertex
                    vertex = mesh.mVertices[ index ]
                    glVertex3f( vertex.x, vertex.y, vertex.z )
                
                glEnd()
            
            # TODO: remove texture
            #glDisable( self.texture.target )
        
        # render the child nodes
        for childIndex in xrange( node.mNumChildren ):
            self.recursive_render( scene, node.mChildren[ childIndex ].contents )
        
        # pop the mesh matrix from the stack
        glPopMatrix()
    
    def render( self ):
        glCallList( self.displayList )
    



def test1():
    import os
    
    #get a model out of assimp's test-data
    #MODEL = r'C:\Users\adam\workspace\python\3d_engine\test_app\src\data\sydney.md2'
    #MODEL = r'C:\Users\adam\workspace\python\3d_engine\BomberCommand\data\meshes\b17\b17g.3ds'
    #MODEL = r'C:\Users\adam\Downloads\development\3d\aircraft\me109\Messerschmitt\Bf109G6.3DS'
    MODEL = r'C:\Users\adam\Downloads\development\3d\aircraft\b17\B-17\b17g.3ds'

    scene = pyassimp.load(MODEL)
    
    #the model we load
    print "MODEL:", MODEL
    print
    
    #write some statistics
    print "SCENE:"
    print "  meshes:", len(scene.meshes)
    print "  materials:", len(scene.materials)
    print "  textures:", len(scene.textures)
    print
    
    print "MESHES:"
    for index, mesh in enumerate(scene.meshes):
        print "  MESH", index+1
        print "    material:", mesh.mMaterialIndex+1
        print "    vertices:", len(mesh.vertices)
        print "    first:", mesh.vertices[:3]
        print "    colors:", len(mesh.colors)
        tc = mesh.texcoords
        print "    texture-coords 1:", len(tc[0]), "first:", tc[0][:3]
        print "    texture-coords 2:", len(tc[1]), "first:", tc[1][:3]
        print "    texture-coords 3:", len(tc[2]), "first:", tc[2][:3]
        print "    texture-coords 4:", len(tc[3]), "first:", tc[3][:3]
        print "    uv-component-count:", len(mesh.mNumUVComponents)
        print "    faces:", len(mesh.faces), "first:", [f.indices for f in mesh.faces[:3]]
        print "    bones:", len(mesh.bones), "first:", [b.mName for b in mesh.bones[:3]]
        print

    print "MATERIALS:"
    for index, material in enumerate(scene.materials):
        print "  MATERIAL", index+1
        properties = pyassimp.GetMaterialProperties(material)
        for key in properties:
            print "    %s: %s" % (key, properties[key])
    print
    
    print "TEXTURES:"
    if scene.textures != None:
        for index, texture in enumerate(scene.textures):
            print "  TEXTURE", index+1
            print "    width:", texture.mWidth
            print "    height:", texture.mHeight
            print "    hint:", texture.achFormatHint
            print "    data (size):", texture.mWidth*texture.mHeight
   
    # Finally release the model
    pyassimp.release(scene)

def test2():
    print 'test2'
    mesh = OAI_Mesh(
        r'C:\Users\adam\Downloads\development\3d\aircraft\me109\Messerschmitt\Bf109G6.3DS'
        #r'C:\Users\adam\Downloads\development\3d\aircraft\b17\B-17\b17g.3ds'
        )
    mesh.load()
    print 'done'


if __name__ == "__main__":
    #test1()
    test2()
