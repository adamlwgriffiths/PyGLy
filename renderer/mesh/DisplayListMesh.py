# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:05:03 2011

@author: adam
"""

import PyGLy.Mesh.Loader as Loader


"""
Mesh
[VBO Vertices, Colours, Normals]
Indices [Type, Indices] [Type, Indices]	where Type is POINT, TRI, QUAD, etc

http://stackoverflow.com/questions/4618892/basic-opengl-vertex-buffers-and-pyglet
http://nehe.gamedev.net/tutorial/model_loading/16004/
http://nehe.gamedev.net/tutorial/vertex_buffer_objects/22002/
http://tartley.com/?p=264
http://www.aida.t.u-tokyo.ac.jp/~saeki/pyglet/doc.en/#graphics
http://pyglet.org/doc/api/pyglet.graphics.vertexbuffer-module.html
http://pyglet.org/doc/api/pyglet.graphics.vertexbuffer.VertexBufferObject-class.html
http://pyglet.org/doc/api/pyglet.graphics.vertexbuffer.VertexArray-class.html
http://pyglet.org/doc/api/pyglet.graphics.vertexbuffer.MappableVertexBufferObject-class.html
"""

class DisplayListMesh( object ):
    
    def __init__( self, filename ):
        super( DisplayListMesh, self ).__init__()
        
        self.filename = filename
        
        self.model = Loader.pyassimp.load( self.filename )
    
    def render( self ):
        pass
    

if __name__ == '__main__':
    print 'loading mesh'
    dlmesh = DisplayListMesh( r'C:\Users\adam\workspace\python\opengl_app\opengl_app\src\data\sydney.md2' )
    print 'loaded'
    
    #write some statistics
    print "SCENE:"
    print "  meshes:", len(dlmesh.model.meshes)
    print "  materials:", len(dlmesh.model.materials)
    print "  textures:", len(dlmesh.model.textures)
    print
    
    print "MESHES:"
    for index, mesh in enumerate(dlmesh.model.meshes):
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
        
        print "INDICES"
        faceNum = 0
        for face in mesh.faces:
            print "Face %i - %s " % (faceNum + 1, face.mNumIndices),
            for indice in face.indices:
                print indice,
            print

    print "MATERIALS:"
    for index, material in enumerate(dlmesh.model.materials):
        print "  MATERIAL", index+1
        properties = Loader.pyassimp.GetMaterialProperties(material)
        for key in properties:
            print "    %s: %s" % (key, properties[key])
    print
    
    print "TEXTURES:"
    for index, texture in enumerate(dlmesh.model.textures):
        print "  TEXTURE", index+1
        print "    width:", texture.mWidth
        print "    height:", texture.mHeight
        print "    hint:", texture.achFormatHint
        print "    data (size):", texture.mWidth*texture.mHeight
   
    # Finally release the model
    Loader.pyassimp.release(dlmesh.model)
