# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:17:02 2011

@author: adam
"""

import os
import struct
from collections import namedtuple

import numpy

class PyMeshException( Exception ):
    pass

class InvalidMeshException( Exception ):
    pass

"""
MD2 Specification
http://tfc.duke.free.fr/coding/md2-specs-en.html

MD2 is in little endian format
"""

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

# frame is composed of 3 float32 vectors
# and a 16 character string
FrameOffsets = struct.Struct( '< 3f 3f' )
FrameName = struct.Struct( '< 16s' )

# OpenGL commands are stored as a +/- integer
# followed by a list of indices
# each indice is 2 floats and a 32-bit integer
OpenGL_Command = struct.Struct( '< 1l' )

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

# The tuple used to store frame data
Frame = namedtuple(
    'Frame',
    [
        'name',
        'vertices',
        'normals'
        ]
    )

Polygon = namedtuple(
    'Polygon',
    [
        'gl_command',
        'indices'
        ]
    )


def loadModel( filename ):
    # this guarantees the file will be closed
    # even if an error occurs
    with open( filename, 'rb' ) as f:
        # read the header
        header = readHeader( f )
        
        # seek to the start of the frames
        f.seek( header.offset_frames, os.SEEK_SET )
        
        # load the animations
        frames = []
        for frameNum in xrange( header.num_frames ):
            frame = readFrame( f, header )
            frames.append( frame )

        # load the texture coordinates
        tcs = readTextureCoordinates( f, header )
        
        # extract the OpenGL commands
        commands = readOpenGL_Commands( f, header )
        
        return frames, tcs, commands

def readOpenGL_Commands( f, header ):
    # seek to the opengl commands offset
    f.seek( header.offset_glcmds, os.SEEK_SET )
    
    commands = []
    #tcs = []
    
    # there is no pre-determined value for the number
    # of OpenGL commands
    # the header.num_glcmds actually indicates the number of
    # 32-bit values in the OpenGL commands block of the file
    while True:
        # read the command, this can be + or -
        # +ve value indicates a GL_TRIANGLE_STRIP
        # -ve value indicates a GL_TRIANGLE_FAN
        # the absolute value is the number of indices for this batch
        command = OpenGL_Command.unpack(
            f.read( OpenGL_Command.size )
            )[ 0 ]
        
        # a 0 command indicates the end of the list
        if command == 0:
            break
        
        # each command has N x 2 32-bit floats and a 32-bit integer
        # the 2 floats are the texture coordinates and the 32-bit
        # integer is the vertex indice.
        # we have to extend the string by the number of vertices
        absCommand = abs( command )
        commandString = ' 2f 1L' * absCommand
        OpenGL_Indice = struct.Struct( '<%s' % commandString )
        
        values = numpy.array(
            OpenGL_Indice.unpack(
                f.read( OpenGL_Indice.size )
                ),
            dtype = numpy.float32
            )
        
        # reshape the array
        values.shape = ( absCommand, 3 )
        
        # pull out the texture coordinates
        #tcs.append( values[ :, 0:1 ] )
        
        # pull out the indices
        floatIndices = values[ :, 2 ]
        
        # convert from float to int
        # http://stackoverflow.com/questions/4389517/in-place-type-conversion-of-a-numpy-array
        intIndices = floatIndices.view( 'int32' )
        intIndices[ : ] = floatIndices
        
        """
        intIndices = numpy.array( values[ :, 2 ], dtype = numpy.int32 )
        """
        polygon = Polygon._make(
            [
                command,
                intIndices
                ]
            )
        
        commands.append( polygon )
    
    # TODO: convert TCs from matching the indice list
    # to matching the vertex list
    #properTCs = tcs[ indices ]
    #print properTCs
    
    return commands

def readTextureCoordinates( f, header ):
    # seek to the texture coordinate offset
    f.seek( header.num_st, os.SEEK_SET )
    
    # Texture coordinates are composed of
    # 2 shorts (2 byte integers) which are then
    # divided by skinwidth and skinheight
    # to get the float values
    TextureCoordinates = struct.Struct(
        '< %ih' % ( header.num_vertices * 2 )
        )
    
    # we'll create the array as floats to begin with so
    # we can do the conversion in place
    tcs = numpy.array(
        TextureCoordinates.unpack( f.read( TextureCoordinates.size ) ),
        dtype = numpy.float32
        )
    
    # convert the coordinates to a 2d array
    tcs.shape = ( header.num_vertices, 2 )
    
    # convert from texels to float 0.0 -> 1.0
    # TU (width) is column 0
    # TV (height) is column 1
    tcs[ :,0 ] /= header.skinwidth
    tcs[ :,1 ] /= header.skinheight
    
    return tcs

def readFrame( f, header ):
    # read the scale and translation
    offsets = numpy.array(
        FrameOffsets.unpack( f.read( FrameOffsets.size ) ),
        dtype = numpy.float32
        )
    # reshape the offsets into 2 vectors
    offsets.shape = ( 2, 3 )
    
    scale = offsets[ 0 ]
    translation = offsets[ 1 ]
    
    # read the frame name
    name = FrameName.unpack( f.read( FrameName.size ) )[ 0 ]
    
    # the \x00 values are confusing python
    # we have to strip them out
    name = name.rstrip( '\x00' )
    
    # vertex made of 3 x,y,z char values and a
    # char normal index
    # we need to create this dynamically due to the changing
    # number of vertices per model
    VertexStruct = struct.Struct(
        '< %iB' % (4 * header.num_vertices)
        )
    
    # put the values into a numpy array
    values = numpy.array(
        VertexStruct.unpack( f.read( VertexStruct.size ) ),
        dtype = numpy.int8
        )
    
    # re-shape the array as Nx4
    values.shape = ( header.num_vertices, 4 )
    
    # pull out the vertices in columns 0 - 2
    # because we're converting from int8 to float32
    # we can't just do a view because of the size difference
    # we need to make a new array and copy it
    vertices = numpy.array( values[ :, 0:3 ], dtype = numpy.float32 )
    
    # apply the scale to the vertices
    vertices *= scale
    # apply the translation to the vertices
    vertices += translation
    
    # pull out the normal indices in column 3
    normalIndices = values[ :, 3 ]
    
    # convert the normal index to the actual values
    normals = Normals[ normalIndices ]
    
    frame = Frame._make( [ name, vertices, normals ] )
    return frame

def readHeader( f ):
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
    
    return header


if __name__ == '__main__':
    model = loadModel(
        r'test_app/data/sydney.md2'
        )
