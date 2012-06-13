# -*- coding: utf-8 -*-
"""
Created on 02/04/2012

@author: adam
"""

import os
import math
import struct
from collections import namedtuple

import numpy

from pyrr import vector


class MD2( object ):
    # The MD2 identifier
    # 'IDP2'
    id = 'IDP2'

    # The expected MD2 version
    version = 8

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
            'vertex_indices',
            'tc_indices'
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
        dtype = numpy.float
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
    
    def __init__( self ):
        super( MD2, self ).__init__()

        self.frames = []

    def load( self, filename ):
        """
        Reads the MD2 data from the existing
        specified filename.

        @param filename: the filename of the md2 file
        to load.
        """
        with open( filename, 'rb' ) as f:
            self.load_from_buffer( f )
    
    def load_from_buffer( self, f ):
        """
        Reads the MD2 data from a stream object.

        Can be called instead of load() if data
        is not present in a file.

        @param f: the stream object, usually a file.
        """
        # read all the data from the file
        self.header = self.read_header( f )
        self.skins = self.read_skins( f, self.header )
        raw_tcs = self.read_texture_coordinates( f, self.header )
        self.triangles = self.read_triangles( f, self.header )
        raw_frames = self.read_frames( f, self.header )

        # convert our tcs to their actual values
        self.tcs = raw_tcs[ self.triangles.tc_indices ]

        # we don't store the raw frame data, instead we'll make
        # rendering faster and convert the frame indices to
        # actual vertices in the index order
        self.frames = self.convert_indicies_for_all_frames(
            raw_frames,
            self.triangles
            )

    @staticmethod
    def _load_block( stream, format, count ):
        """
        Convenience method used to load blocks of
        data using the python 'struct' object format.

        Loads 'count' blocks from the file, each block
        will have the python struct format defined by 'format'.
        This is handy for loading large blocks without having
        to manually iterate over it.

        @param stream: the file object.
        @param format: the python 'struct' format of the block.
        @param count: the number of blocks to load.
        """
        def chunks( data, size ):
            """
            Return a generator that yields next 'size' bytes from data
            """
            offset = 0
            while offset < len( data ):
                yield data[ offset: offset + size ]
                offset += size

        struct_length = struct.calcsize( format )
        total_length = struct_length * count
        data = stream.read( total_length )

        if len( data ) < total_length:
            raise ValueError( "MD2: Failed to read '%d' bytes" % (total_length) )

        return [ struct.unpack(format, chunk) for chunk in chunks(data, struct_length) ]

    @staticmethod
    def read_header( f ):
        """
        Reads the MD2 header information from the MD2 file.

        @param f: the file object.
        @return Returns an header_layout named tuple.
        """
        # read the header
        # header is made up of 17 signed longs
        # this first is the ID which is also a 4 byte string
        header = MD2.header_layout._make(
            MD2._load_block( f, '< 4s16l', 1 )[ 0 ]
            )

        if header.ident != MD2.id:
            raise ValueError(
                "MD2 identifier is incorrect, expected '%i', found '%i'" % (
                    MD2.id,
                    header.ident
                    )
                )
        if header.version != MD2.version:
            raise ValueError(
                "MD2 version is incorrect, expected '%i', found '%i'" % (
                    MD2.version,
                    header.version
                    )
                )

        return header

    @staticmethod
    def read_skins( f, header ):
        """
        Reads the skin filenames out of the MD2 header.

        @param f: the file object.
        @param header: the loaded MD2 header.
        @return: Returns a python list of skin filenames.
        The list is a 1D list of size header.num_skins.
        """
        # seek to the skins offset
        f.seek( header.offset_skins, os.SEEK_SET )

        # skins are stored as a list of 64 signed byte strings
        # each string is a path relative to /baseq2
        skin_struct = struct.Struct( '< %s' % ('64s' * header.num_skins) )

        # read the skins and convert to list
        # strip any \x00 characters while we're at it
        # because python gets confused by them
        return [ skin.rstrip('\x00') for skin in skin_struct.unpack( f.read( skin_struct.size ) ) ]

    @staticmethod
    def read_texture_coordinates( f, header ):
        """
        Reads the texture coordinates from the MD2 file.

        @param f: the file object.
        @param header: the loaded MD2 header.
        @return: Returns a numpy array containing the texture
        coordinates. Values are converted from original
        absolute texels (0->width,0->height) to openGL
        coordinates (0.0->1.0).
        The array is an Nx2 dimension array where N
        is header.num_st.
        """
        # seek to the skins offset
        f.seek( header.offset_st, os.SEEK_SET )

        # st's are stored in a contiguous array of 2 short values
        # TCs do NOT map directly to vertices.
        # 1 vertex can have multiple TCs (one TC for each poly)
        # TCs are composed of 2 signed shorts
        tcs = numpy.array(
            MD2._load_block( f, '< 2h', header.num_st ),
            dtype = numpy.float
            )
        tcs.shape = (-1, 2)

        # convert from texel values to 0->1 float range
        tcs /= [ float(header.skin_width), float(header.skin_height) ]
        return tcs

    @staticmethod
    def read_triangles( f, header ):
        """
        Reads the triangle information from the MD2 file.

        Triangle information includes the vertex and
        texture coordinate indices.

        @param f: the file object.
        @param header: the loaded MD2 header.
        @return: Returns an MD2 named tuple.
        The vertex and texture coordinate indices are
        arrays of Nx3 dimensions where N is header.num_tris.
        """
        # seek to the triangles offset
        f.seek( header.offset_tris, os.SEEK_SET )

        # triangles are stored as 3 unsigned shorts for the vertex indices
        # and 3 unsigned shorts for the texture coordinates indices
        triangles = numpy.array(
            MD2._load_block( f, '< 6H', header.num_tris ),
            dtype = numpy.uint16
            )
        triangles.shape = (-1, 6)

        # extract the vertex indices and tcs
        vertex_indices = triangles[ : , :3 ]
        tc_indices = triangles[ : , 3: ]

        # md2 triangles are clock-wise, we need to change
        # them to counter-clock-wise
        vertex_indices[ :,[1,2] ] = vertex_indices[ :,[2,1] ]
        tc_indices[ :,[1,2] ] = tc_indices[ :,[2,1] ]

        vertex_indices = vertex_indices.flatten()
        tc_indices = tc_indices.flatten()

        triangles = MD2.triangle_layout._make(
            [ vertex_indices, tc_indices ]
            )

        return triangles

    @staticmethod
    def read_frames( f, header ):
        """
        Reads all frames from the MD2 file.

        This function simply calls read_frame in a loop.

        @param f: the file object.
        @param header: the loaded MD2 header.
        @return returns a python list of frame_layout
        named tuples. The list will be of length
        header.num_frames.
        """
        # seek to the frames offset
        f.seek( header.offset_frames, os.SEEK_SET )
        return [ MD2.read_frame( f, header ) for x in xrange( header.num_frames ) ]

    @staticmethod
    def read_frame( f, header ):
        """
        Reads a frame from the MD2 file.

        The stream must already be at the start of the
        frame.

        @param f: the file object.
        @param header: the loaded MD2 header.
        @return: Returns an frame_layout named tuple.
        Returned vertices and normals are as read from
        the file and are not ready to render.
        To render these must be ordered according to
        the indices specified in the triangle information.

        @see convert_indices_for_all_frames
        @see convert_indices_for_frame
        """
        # frame scale and translation are 2x3 32 bit floats
        frame_translations = numpy.array(
            MD2._load_block( f, '< 3f', 2 ),
            dtype = numpy.float
            )
        # extract the scale and translation vector
        scale = frame_translations[ 0 ]
        translation = frame_translations[ 1 ]

        # read the frame name
        # frame name is a 16 unsigned byte string
        name, = MD2._load_block( f, '< 16s', 1 )[0]
        # remove any \x00 characters as they confuse python
        name = name.strip( '\x00' )

        # frame has 3 unsigned bytes for the vertex coordinates
        # and 1 unsigned byte for the normal index
        frame_vertex_data = numpy.array(
            MD2._load_block( f, '<4B', header.num_vertices ),
            dtype = numpy.uint8
            )
        frame_vertex_data.shape = (-1, 4)

        # extract the vertex values
        vertices_short = frame_vertex_data[ :, :3 ]
        vertices = vertices_short.astype( numpy.float )
        vertices.shape = (-1, 3)

        # apply the frame translation
        vertices *= scale
        vertices += translation

        # re-orient the mesh
        # md2's have +Z as up, +Y as left, +X as forward
        # up: +Z, left: +Y, forward: +X
        # we want
        # up: +Y, left: -X, forward: -Z
        vertices[:,0],vertices[:,1],vertices[:,2] = \
            -vertices[:,1],vertices[:,2],-vertices[:,0]

        # extract the normal values
        normal_indices = frame_vertex_data[ :, 3 ]
        # convert from normal indice to normal vector
        normals = MD2.normal_lookup_table[ normal_indices ]
        normals.shape = (-1, 3)

        return MD2.frame_layout._make(
            [ name, vertices, normals ]
            )

    @staticmethod
    def convert_indicies_for_all_frames( frames, triangles ):
        """
        Creates vertex lists for all frames.

        This function essentially calls
        'convert_indices_for_frame' for all frames.

        @param frames: the list of frames.
        @param triangles: the list of triangles.
        @return: returns a python list containing
        frame_layout named tuples.
        The list will be header.num_frames in length.
        """
        return [ MD2.convert_indices_for_frame( frame, triangles ) for frame in frames ]

    @staticmethod
    def convert_indices_for_frame( frame, triangles ):
        """
        Creates a vertex list ready for rendering from
        the loaded data.

        Takes the frame's vertices and normals and
        converts them to a vertex list using the
        extracted triangle indices.

        @param frame: the frame to convert.
        @param triangles: the triangle data containing the
        indices.
        @return: returns a frame_layout named tuple with
        the converted data.
        """
        return MD2.frame_layout._make(
            [
                frame.name,
                frame.vertices[ triangles.vertex_indices ],
                frame.normals[ triangles.vertex_indices ]
                ]
            )

