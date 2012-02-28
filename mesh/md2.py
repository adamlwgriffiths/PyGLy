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
id = 844121161

# The expected MD2 version
version = 8

# header is made up of 17 4-byte integers
header_layout = namedtuple(
    'MD2_Header',
    [
        'ident',
        'version',
        'skin_width',
        'skin_height',
        'frame_size',
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
header_struct = struct.Struct( '< 17L' )

opengl_command_struct = struct.Struct( '< 1l' )

opengl_command_data_struct = struct.Struct( '< 2f 1l' )

vector_struct = struct.Struct( '< 3f' )
frame_name_struct = struct.Struct( '< 16s' )

frame_vertex_struct = struct.Struct( '< 4B' )

frame_layout = namedtuple(
    'MD2_Frame',
    [
        'name',
        'vertices',
        'normals'
        ]
    )

triangle_layout = namedtuple(
    'MD2_Triangles',
    [
        'indices',
        'tcs'
        ]
    )

opengl_command = namedtuple(
    'MD2_GL_Command',
    [
        'type',
        'indices',
        'tcs'
        ]
    )

model_layout = namedtuple(
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
normal_lookup_table = numpy.array(
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
frame_names = [
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

frame_offsets = [
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
        header = read_header( f )
        skins = read_skins( f, header )
        
        tcsList = read_texture_coordinates( f, header )
        triangles = read_triangles( f, header, tcsList )
        
        glCommands = read_gl_commands( f, header )
        
        frames = read_frames( f, header )
    
    md2 = model_layout._make(
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

def read_header( f ):
    # read the header struct from the file
    header = header_layout._make(
        header_struct.unpack( f.read( header_struct.size ) )
        )
    
    if header.ident != id:
        raise InvalidMeshException(
            'MD2 identifier is incorrect: %i' % (header.ident)
            )
    if header.version != version:
        raise InvalidMeshException(
            'MD2 version is incorrect: %i' % (header.version)
            )
    
    #print header
    return header

def read_skins( f, header ):
    # seek to the skins offset
    f.seek( header.offset_skins, os.SEEK_SET )
    
    # skins are stored as a contiguous list of 64 char strings
    # each string is a path relative to /baseq2
    skin_struct = struct.Struct( '< %s' % ('64s' * header.num_skins) )
    
    # read the skins and convert to list
    # strip any \x00 characters while we're at it
    # because python gets confused by them
    skins = [ skin.rstrip('\x00') for skin in skin_struct.unpack( f.read( skin_struct.size ) ) ]
    
    #print skins
    return skins

def read_texture_coordinates( f, header ):
    # seek to the skins offset
    f.seek( header.offset_st, os.SEEK_SET )
    
    # st's are stored in a contiguous array of 2 short values
    # all docs state these are signed
    # but they also state the values are 0 < x < skinMax
    # for some reason, TCs don't map directly to vertices!
    st_struct = struct.Struct( '< %iH' % ( 2 * header.num_st ) )
    
    tcs = numpy.array(
        st_struct.unpack( f.read( st_struct.size ) ),
        dtype = numpy.float32
        )
    tcs.shape = (header.num_st, 2)
    
    tcs /= [ header.skin_width, header.skin_height ]
    
    #print tcs
    return tcs

def read_triangles( f, header, tcs ):
    # seek to the triangles offset
    f.seek( header.offset_tris, os.SEEK_SET )
    
    # triangles are stored as 3 unsigned shorts for the vertex indices
    # and 3 unsigned shorts for the texture coordinates indices
    tri_struct = struct.Struct( '< %iH' % ( 6 * header.num_tris ) )
    
    tris = numpy.array(
        tri_struct.unpack( f.read( tri_struct.size ) ),
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
    tc_index = tris[ : , 3: ]
    #print tcIndex
    tcs = tcs[ tc_index ]
    #print tcs
    
    triangles = triangle_layout._make(
        [
            indices,
            tcs
            ]
        )
    
    return triangles

def read_gl_commands( f, header ):
    # seek to the gl commands offset
    f.seek( header.offset_glcmds, os.SEEK_SET )
    
    # we'll store the commands in a normal list
    commands = []
    
    # iterate through the list of GL commands
    while True:
        # commands are stored as 2 floats for the texture coordinates
        # and an int for the vertex indice
        command_type = opengl_command_struct.unpack(
            f.read( opengl_command_struct.size )
            )[ 0 ]
        
        # if the command is 0, we've hit the end
        if command_type == 0:
            break
        
        # the absolute value of the command is the number
        # of indices
        num_commands = abs( command_type )
        
        # store the indices in a numpy array
        # because we know the length already
        indices = numpy.empty(
            ( num_commands ),
            dtype = numpy.uint32
            )
        
        # we'll convert our tcs into a flat array
        # we have to do this per gl command because
        # some vertices have multiple texture coordinates
        tcs = numpy.empty(
            ( num_commands, 2 ),
            dtype = numpy.float32
            )
        
        # load each commands data
        for num in xrange( num_commands ):
            # the data is mixed int and floats so we can't simply
            # load into a numpy array
            values = opengl_command_data_struct.unpack(
                f.read( opengl_command_data_struct.size )
                )
            
            # add the indice to our command list
            indices[ num ] = values[ 2 ]
            
            # pull out the TCs and put them into our TC
            # array at the position of the vertex indice
            tcs[ (num, 0) ] = values[ 0 ]
            tcs[ (num, 1) ] = values[ 1 ]
        
        # create a named tuple for the command
        # because we're getting pretty complex
        command = opengl_command._make(
            [
                command_type,
                indices,
                tcs
                ]
            )
        # add the command to our list
        commands.append( command )
    
    #print commands
    #print tcs
    
    return commands

def read_frames( f, header ):
    # seek to the gl commands offset
    f.seek( header.offset_frames, os.SEEK_SET )
    
    frames = []
    
    for frame_num in xrange( header.num_frames ):
        frames.append( read_frame( f, header ) )
    
    return frames

def read_frame( f, header ):
    scale = numpy.empty( (3), dtype = numpy.float32 )
    translation = numpy.empty( (3), dtype = numpy.float32 )
    
    vertices = numpy.empty(
        (header.num_vertices, 3),
        dtype = numpy.float32
        )
    normal_indices = []
    
    # read the scale vector
    scale[:] = vector_struct.unpack(
        f.read( vector_struct.size )
        )
    # read the translation vector
    translation[:] = vector_struct.unpack(
        f.read( vector_struct.size )
        )
    # read the frame name
    name = frame_name_struct.unpack(
        f.read( frame_name_struct.size )
        )[ 0 ]
    
    # remove any \x00 characters
    # as they confuse python
    name = name.strip( '\x00' )
    
    #print name
    
    for vertex_num in xrange( header.num_vertices ):
        vertex_values = frame_vertex_struct.unpack(
            f.read( frame_vertex_struct.size )
            )
        
        # read the normal index
        normal_indices.append( vertex_values[ 3 ] )
        vertices[ vertex_num ] = vertex_values[ :3 ]
    
    # convert the normals from a list of indices
    # to the normals themselves
    normals = normal_lookup_table[ normal_indices ]
    
    # apply our scale and translation
    # to our vertices
    vertices *= scale
    vertices += translation
    
    #print vertices
    #print normals
    
    return frame_layout._make(
        [
            name,
            vertices,
            normals
            ]
        )

if __name__ == '__main__':
    model = load(
        r'../test_app/data/sydney.md2'
        )

