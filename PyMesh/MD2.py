# -*- coding: utf-8 -*-
"""
MD2 model format loader.

Created on Sun Sep 11 11:14:20 2011

http://tfc.duke.free.fr/coding/md2-specs-en.html
http://www.icculus.org/homepages/phaethon/q3/formats/md2-schoenblum.html

@author: adam
"""

import os
import struct
from collections import namedtuple

import numpy


# The MD2 identifier
ID = 844121161

# The expected MD2 version
Version = 8

# header is made up of 17 4-byte integers
Header = namedtuple(
    'MD2_Header',
    [
        'ident',
        'version',
        'skinwidth',
        'skinheight',
        'framesize',
        'num_skins',
        'num_vertices',
        'num_st',
        'num_tris',
        'num_glcmds',
        'num_frames',
        'offset_skins',
        'offset_st',
        'offset_tris',
        'offset_frames',
        'offset_glcmds',
        'offset_end'
        ]
    )
HeaderStruct = struct.Struct( '< 17L' )

OpenGL_CommandStruct = struct.Struct( '< 1l' )

OpenGL_CommandDataStruct = struct.Struct( '< 2f 1l' )

Vector = struct.Struct( '< 3f' )
FrameName = struct.Struct( '< 16s' )

FrameVertexStruct = struct.Struct( '< 4B' )

Frame = namedtuple(
    'MD2_Frame',
    [
        'name',
        'vertices',
        'normals'
        ]
    )

Triangles = namedtuple(
    'MD2_Triangles',
    [
        'indices',
        'tcs'
        ]
    )

OpenGL_Command = namedtuple(
    'MD2_GL_Command',
    [
        'type',
        'indices',
        'tcs'
        ]
    )

Model = namedtuple(
    'MD2_Model',
    [
        'filename',
        'header',
        'skins',
        'triangles',
        'gl_primitives',
        'frames'
        ]
    )

# The MD2 normal look-up table
Normals = numpy.array(
    [
        [-0.525731, 0.000000, 0.850651 ],
        [-0.442863, 0.238856, 0.864188 ],
        [-0.295242, 0.000000, 0.955423 ],
        [-0.309017, 0.500000, 0.809017 ],
        [-0.162460, 0.262866, 0.951056 ],
        [ 0.000000, 0.000000, 1.000000 ],
        [ 0.000000, 0.850651, 0.525731 ],
        [-0.147621, 0.716567, 0.681718 ],
        [ 0.147621, 0.716567, 0.681718 ],
        [ 0.000000, 0.525731, 0.850651 ],
        [ 0.309017, 0.500000, 0.809017 ],
        [ 0.525731, 0.000000, 0.850651 ],
        [ 0.295242, 0.000000, 0.955423 ],
        [ 0.442863, 0.238856, 0.864188 ],
        [ 0.162460, 0.262866, 0.951056 ],
        [-0.681718, 0.147621, 0.716567 ],
        [-0.809017, 0.309017, 0.500000 ],
        [-0.587785, 0.425325, 0.688191 ],
        [-0.850651, 0.525731, 0.000000 ],
        [-0.864188, 0.442863, 0.238856 ],
        [-0.716567, 0.681718, 0.147621 ],
        [-0.688191, 0.587785, 0.425325 ],
        [-0.500000, 0.809017, 0.309017 ],
        [-0.238856, 0.864188, 0.442863 ],
        [-0.425325, 0.688191, 0.587785 ],
        [-0.716567, 0.681718,-0.147621 ],
        [-0.500000, 0.809017,-0.309017 ],
        [-0.525731, 0.850651, 0.000000 ],
        [ 0.000000, 0.850651,-0.525731 ],
        [-0.238856, 0.864188,-0.442863 ],
        [ 0.000000, 0.955423,-0.295242 ],
        [-0.262866, 0.951056,-0.162460 ],
        [ 0.000000, 1.000000, 0.000000 ],
        [ 0.000000, 0.955423, 0.295242 ],
        [-0.262866, 0.951056, 0.162460 ],
        [ 0.238856, 0.864188, 0.442863 ],
        [ 0.262866, 0.951056, 0.162460 ],
        [ 0.500000, 0.809017, 0.309017 ],
        [ 0.238856, 0.864188,-0.442863 ],
        [ 0.262866, 0.951056,-0.162460 ],
        [ 0.500000, 0.809017,-0.309017 ],
        [ 0.850651, 0.525731, 0.000000 ],
        [ 0.716567, 0.681718, 0.147621 ],
        [ 0.716567, 0.681718,-0.147621 ],
        [ 0.525731, 0.850651, 0.000000 ],
        [ 0.425325, 0.688191, 0.587785 ],
        [ 0.864188, 0.442863, 0.238856 ],
        [ 0.688191, 0.587785, 0.425325 ],
        [ 0.809017, 0.309017, 0.500000 ],
        [ 0.681718, 0.147621, 0.716567 ],
        [ 0.587785, 0.425325, 0.688191 ],
        [ 0.955423, 0.295242, 0.000000 ],
        [ 1.000000, 0.000000, 0.000000 ],
        [ 0.951056, 0.162460, 0.262866 ],
        [ 0.850651,-0.525731, 0.000000 ],
        [ 0.955423,-0.295242, 0.000000 ],
        [ 0.864188,-0.442863, 0.238856 ],
        [ 0.951056,-0.162460, 0.262866 ],
        [ 0.809017,-0.309017, 0.500000 ],
        [ 0.681718,-0.147621, 0.716567 ],
        [ 0.850651, 0.000000, 0.525731 ],
        [ 0.864188, 0.442863,-0.238856 ],
        [ 0.809017, 0.309017,-0.500000 ],
        [ 0.951056, 0.162460,-0.262866 ],
        [ 0.525731, 0.000000,-0.850651 ],
        [ 0.681718, 0.147621,-0.716567 ],
        [ 0.681718,-0.147621,-0.716567 ],
        [ 0.850651, 0.000000,-0.525731 ],
        [ 0.809017,-0.309017,-0.500000 ],
        [ 0.864188,-0.442863,-0.238856 ],
        [ 0.951056,-0.162460,-0.262866 ],
        [ 0.147621, 0.716567,-0.681718 ],
        [ 0.309017, 0.500000,-0.809017 ],
        [ 0.425325, 0.688191,-0.587785 ],
        [ 0.442863, 0.238856,-0.864188 ],
        [ 0.587785, 0.425325,-0.688191 ],
        [ 0.688191, 0.587785,-0.425325 ],
        [-0.147621, 0.716567,-0.681718 ],
        [-0.309017, 0.500000,-0.809017 ],
        [ 0.000000, 0.525731,-0.850651 ],
        [-0.525731, 0.000000,-0.850651 ],
        [-0.442863, 0.238856,-0.864188 ],
        [-0.295242, 0.000000,-0.955423 ],
        [-0.162460, 0.262866,-0.951056 ],
        [ 0.000000, 0.000000,-1.000000 ],
        [ 0.295242, 0.000000,-0.955423 ],
        [ 0.162460, 0.262866,-0.951056 ],
        [-0.442863,-0.238856,-0.864188 ],
        [-0.309017,-0.500000,-0.809017 ],
        [-0.162460,-0.262866,-0.951056 ],
        [ 0.000000,-0.850651,-0.525731 ],
        [-0.147621,-0.716567,-0.681718 ],
        [ 0.147621,-0.716567,-0.681718 ],
        [ 0.000000,-0.525731,-0.850651 ],
        [ 0.309017,-0.500000,-0.809017 ],
        [ 0.442863,-0.238856,-0.864188 ],
        [ 0.162460,-0.262866,-0.951056 ],
        [ 0.238856,-0.864188,-0.442863 ],
        [ 0.500000,-0.809017,-0.309017 ],
        [ 0.425325,-0.688191,-0.587785 ],
        [ 0.716567,-0.681718,-0.147621 ],
        [ 0.688191,-0.587785,-0.425325 ],
        [ 0.587785,-0.425325,-0.688191 ],
        [ 0.000000,-0.955423,-0.295242 ],
        [ 0.000000,-1.000000, 0.000000 ],
        [ 0.262866,-0.951056,-0.162460 ],
        [ 0.000000,-0.850651, 0.525731 ],
        [ 0.000000,-0.955423, 0.295242 ],
        [ 0.238856,-0.864188, 0.442863 ],
        [ 0.262866,-0.951056, 0.162460 ],
        [ 0.500000,-0.809017, 0.309017 ],
        [ 0.716567,-0.681718, 0.147621 ],
        [ 0.525731,-0.850651, 0.000000 ],
        [-0.238856,-0.864188,-0.442863 ],
        [-0.500000,-0.809017,-0.309017 ],
        [-0.262866,-0.951056,-0.162460 ],
        [-0.850651,-0.525731, 0.000000 ],
        [-0.716567,-0.681718,-0.147621 ],
        [-0.716567,-0.681718, 0.147621 ],
        [-0.525731,-0.850651, 0.000000 ],
        [-0.500000,-0.809017, 0.309017 ],
        [-0.238856,-0.864188, 0.442863 ],
        [-0.262866,-0.951056, 0.162460 ],
        [-0.864188,-0.442863, 0.238856 ],
        [-0.809017,-0.309017, 0.500000 ],
        [-0.688191,-0.587785, 0.425325 ],
        [-0.681718,-0.147621, 0.716567 ],
        [-0.442863,-0.238856, 0.864188 ],
        [-0.587785,-0.425325, 0.688191 ],
        [-0.309017,-0.500000, 0.809017 ],
        [-0.147621,-0.716567, 0.681718 ],
        [-0.425325,-0.688191, 0.587785 ],
        [-0.162460,-0.262866, 0.951056 ],
        [ 0.442863,-0.238856, 0.864188 ],
        [ 0.162460,-0.262866, 0.951056 ],
        [ 0.309017,-0.500000, 0.809017 ],
        [ 0.147621,-0.716567, 0.681718 ],
        [ 0.000000,-0.525731, 0.850651 ],
        [ 0.425325,-0.688191, 0.587785 ],
        [ 0.587785,-0.425325, 0.688191 ],
        [ 0.688191,-0.587785, 0.425325 ],
        [-0.955423, 0.295242, 0.000000 ],
        [-0.951056, 0.162460, 0.262866 ],
        [-1.000000, 0.000000, 0.000000 ],
        [-0.850651, 0.000000, 0.525731 ],
        [-0.955423,-0.295242, 0.000000 ],
        [-0.951056,-0.162460, 0.262866 ],
        [-0.864188, 0.442863,-0.238856 ],
        [-0.951056, 0.162460,-0.262866 ],
        [-0.809017, 0.309017,-0.500000 ],
        [-0.864188,-0.442863,-0.238856 ],
        [-0.951056,-0.162460,-0.262866 ],
        [-0.809017,-0.309017,-0.500000 ],
        [-0.681718, 0.147621,-0.716567 ],
        [-0.681718,-0.147621,-0.716567 ],
        [-0.850651, 0.000000,-0.525731 ],
        [-0.688191, 0.587785,-0.425325 ],
        [-0.587785, 0.425325,-0.688191 ],
        [-0.425325, 0.688191,-0.587785 ],
        [-0.425325,-0.688191,-0.587785 ],
        [-0.587785,-0.425325,-0.688191 ],
        [-0.688191,-0.587785,-0.425325 ]
    ],
    dtype = numpy.float32
    )

# List of frame types used by Quake 2
# http://tfc.duke.free.fr/old/models/md2.htm
FrameNames = [
    'stand',
    'run',
    'attack',
    'pain_a',
    'pain_b',
    'pain_c',
    'jump',
    'flip',
    'salute',
    'fallback',
    'wave',
    'point',
    'crouch_stand',
    'crouch_walk',
    'crouch_attack',
    'crouch_pain',
    'crouch_death', 
    'death_fallback',
    'death_fallforward',
    'death_fallbackslow',
    'boom',
    ]

FrameInfo = [
    # start frame, end frame, fps
    (   0,  39,  9.0 ),   # STAND
    (  40,  45, 10.0 ),   # RUN
    (  46,  53, 10.0 ),   # ATTACK
    (  54,  57,  7.0 ),   # PAIN_A
    (  58,  61,  7.0 ),   # PAIN_B
    (  62,  65,  7.0 ),   # PAIN_C
    (  66,  71,  7.0 ),   # JUMP
    (  72,  83,  7.0 ),   # FLIP
    (  84,  94,  7.0 ),   # SALUTE
    (  95, 111, 10.0 ),   # FALLBACK
    ( 112, 122,  7.0 ),   # WAVE
    ( 123, 134,  6.0 ),   # POINT
    ( 135, 153, 10.0 ),   # CROUCH_STAND
    ( 154, 159,  7.0 ),   # CROUCH_WALK
    ( 160, 168, 10.0 ),   # CROUCH_ATTACK
    ( 196, 172,  7.0 ),   # CROUCH_PAIN
    ( 173, 177,  5.0 ),   # CROUCH_DEATH
    ( 178, 183,  7.0 ),   # DEATH_FALLBACK
    ( 184, 189,  7.0 ),   # DEATH_FALLFORWARD
    ( 190, 197,  7.0 ),   # DEATH_FALLBACKSLOW
    ( 198, 198,  5.0 ),   # BOOM
    ]


class InvalidMeshException( Exception ):
    pass


def load( filename ):
    # this guarantees the file will be closed
    # even if an error occurs
    with open( filename, 'rb' ) as f:
        # read the header
        header = readHeader( f )
        skins = readSkins( f, header )
        
        tcsList = readTextureCoordinates( f, header )
        triangles = readTriangles( f, header, tcsList )
        
        glCommands = readGL_Commands( f, header )
        
        frames = readFrames( f, header )
    
    md2 = Model._make(
        [
            filename,
            header,
            skins,
            triangles,
            glCommands,
            frames
            ]
        )
    
    return md2

def readHeader( f ):
    # read the header struct from the file
    header = Header._make(
        HeaderStruct.unpack( f.read( HeaderStruct.size ) )
        )
    
    if header.ident != ID:
        raise InvalidMeshException(
            'MD2 identifier is incorrect: %i' % (header.ident)
            )
    if header.version != Version:
        raise InvalidMeshException(
            'MD2 version is incorrect: %i' % (header.version)
            )
    
    #print header
    return header

def readSkins( f, header ):
    # seek to the skins offset
    f.seek( header.offset_skins, os.SEEK_SET )
    
    # skins are stored as a contiguous list of 64 char strings
    # each string is a path relative to /baseq2
    SkinStruct = struct.Struct( '< %s' % ('64s' * header.num_skins) )
    
    # read the skins and convert to list
    # strip any \x00 characters while we're at it
    # because python gets confused by them
    skins = [ skin.rstrip('\x00') for skin in SkinStruct.unpack( f.read( SkinStruct.size ) ) ]
    
    #print skins
    return skins

def readTextureCoordinates( f, header ):
    # seek to the skins offset
    f.seek( header.offset_st, os.SEEK_SET )
    
    # st's are stored in a contiguous array of 2 short values
    # all docs state these are signed
    # but they also state the values are 0 < x < skinMax
    # for some reason, TCs don't map directly to vertices!
    ST_Struct = struct.Struct( '< %iH' % ( 2 * header.num_st ) )
    
    tcs = numpy.array(
        ST_Struct.unpack( f.read( ST_Struct.size ) ),
        dtype = numpy.float32
        )
    tcs.shape = (header.num_st, 2)
    
    tcs /= [ header.skinwidth, header.skinheight ]
    
    #print tcs
    return tcs

def readTriangles( f, header, tcs ):
    # seek to the triangles offset
    f.seek( header.offset_tris, os.SEEK_SET )
    
    # triangles are stored as 3 unsigned shorts for the vertex indices
    # and 3 unsigned shorts for the texture coordinates indices
    TriStruct = struct.Struct( '< %iH' % ( 6 * header.num_tris ) )
    
    tris = numpy.array(
        TriStruct.unpack( f.read( TriStruct.size ) ),
        dtype = numpy.uint8
        )
    tris.shape = ( header.num_tris, 6 )
    
    #print tris
    
    # extract the triangle indices
    indices = tris[ : , :3 ]
    #print indices
    
    # the triangles are indices into our vertex and
    # texture coorindate arrays.
    # so we should convert the tcs to be associate with
    # each vertex
    tcIndex = tris[ : , 3: ]
    #print tcIndex
    tcs = tcs[ tcIndex ]
    #print tcs
    
    triangles = Triangles._make(
        [
            indices,
            tcs
            ]
        )
        
    
    return triangles

def readGL_Commands( f, header ):
    # seek to the gl commands offset
    f.seek( header.offset_glcmds, os.SEEK_SET )
    
    # we'll store the commands in a normal list
    commands = []
    
    # iterate through the list of GL commands
    while True:
        # commands are stored as 2 floats for the texture coordinates
        # and an int for the vertex indice
        commandType = OpenGL_CommandStruct.unpack(
            f.read( OpenGL_CommandStruct.size )
            )[ 0 ]
        
        # if the command is 0, we've hit the end
        if commandType == 0:
            break
        
        # the absolute value of the command is the number
        # of indices
        numCommands = abs( commandType )
        
        # store the indices in a numpy array
        # because we know the length already
        indices = numpy.empty(
            ( numCommands ),
            dtype = numpy.uint32
            )
        
        # we'll convert our tcs into a flat array
        # we have to do this per gl command because
        # some vertices have multiple texture coordinates
        tcs = numpy.empty(
            ( numCommands, 2 ),
            dtype = numpy.float32
            )
        
        # load each commands data
        for num in xrange( numCommands ):
            # the data is mixed int and floats so we can't simply
            # load into a numpy array
            values = OpenGL_CommandDataStruct.unpack(
                f.read( OpenGL_CommandDataStruct.size )
                )
            
            # add the indice to our command list
            indices[ num ] = values[ 2 ]
            
            # pull out the TCs and put them into our TC
            # array at the position of the vertex indice
            tcs[ (num, 0) ] = values[ 0 ]
            tcs[ (num, 1) ] = values[ 1 ]
        
        # create a named tuple for the command
        # because we're getting pretty complex
        command = OpenGL_Command._make(
            [
                commandType,
                indices,
                tcs
                ]
            )
        # add the command to our list
        commands.append( command )
    
    #print commands
    #print tcs
    
    return commands

def readFrames( f, header ):
    # seek to the gl commands offset
    f.seek( header.offset_frames, os.SEEK_SET )
    
    frames = []
    
    for frameNum in xrange( header.num_frames ):
        frames.append( readFrame( f, header ) )
    
    return frames

def readFrame( f, header ):
    scale = numpy.empty( (3), dtype = numpy.float32 )
    translation = numpy.empty( (3), dtype = numpy.float32 )
    
    vertices = numpy.empty(
        (header.num_vertices, 3),
        dtype = numpy.float32
        )
    normalIndices = []
    
    # read the scale vector
    scale[:] = Vector.unpack(
        f.read( Vector.size )
        )
    # read the translation vector
    translation[:] = Vector.unpack(
        f.read( Vector.size )
        )
    # read the frame name
    name = FrameName.unpack(
        f.read( FrameName.size )
        )[ 0 ]
    
    # remove any \x00 characters
    # as they confuse python
    name = name.strip( '\x00' )
    
    #print name
    
    for vertexNum in xrange( header.num_vertices ):
        vertexValues = FrameVertexStruct.unpack(
            f.read( FrameVertexStruct.size )
            )
        
        # read the normal index
        normalIndices.append( vertexValues[ 3 ] )
        vertices[ vertexNum ] = vertexValues[ :3 ]
    
    # convert the normals from a list of indices
    # to the normals themselves
    normals = Normals[ normalIndices ]
    
    # apply our scale and translation
    # to our vertices
    vertices *= scale
    vertices += translation
    
    #print vertices
    #print normals
    
    return Frame._make(
        [
            name,
            vertices,
            normals
            ]
        )

if __name__ == '__main__':
    model = load(
        r'C:\Users\adam\workspace\python\opengl_app\opengl_app\src\data\sydney.md2'
        )
