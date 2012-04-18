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
from pyglet.gl import *

from pygly.maths import vector


class MD2_Mesh( object ):
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
    
    def __init__( self, filename ):
        super( MD2_Mesh, self ).__init__()
        
        self.filename = filename
        self.frame = 0.0
        self.frames = []

    def load( self ):
        with open( self.filename, 'rb' ) as f:
            self.load_from_buffer( f )
    
    def load_from_buffer( self, f ):
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
        Loads 'count' structs of 'format' from the steam.
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
            raise ValueError( "MD2_Mesh: Failed to read '%d' bytes" % (total_length) )

        return [ struct.unpack(format, chunk) for chunk in chunks(data, struct_length) ]

    @staticmethod
    def read_header( f ):
        # read the header
        # header is made up of 17 signed longs
        # this first is the ID which is also a 4 byte string
        header = MD2_Mesh.header_layout._make(
            MD2_Mesh._load_block( f, '< 4s16l', 1 )[ 0 ]
            )

        if header.ident != MD2_Mesh.id:
            raise ValueError(
                "MD2 identifier is incorrect, expected '%i', found '%i'" % (
                    MD2_Mesh.id,
                    header.ident
                    )
                )
        if header.version != MD2_Mesh.version:
            raise ValueError(
                "MD2 version is incorrect, expected '%i', found '%i'" % (
                    MD2_Mesh.version,
                    header.version
                    )
                )

        return header

    @staticmethod
    def read_skins( f, header ):
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
        # seek to the skins offset
        f.seek( header.offset_st, os.SEEK_SET )

        # st's are stored in a contiguous array of 2 short values
        # TCs do NOT map directly to vertices.
        # 1 vertex can have multiple TCs (one TC for each poly)
        # TCs are composed of 2 signed shorts
        tcs = numpy.array(
            MD2_Mesh._load_block( f, '< 2h', header.num_st ),
            dtype = numpy.float
            )
        tcs.shape = (-1, 2)

        # convert from texel values to 0->1 float range
        tcs /= [ float(header.skin_width), float(header.skin_height) ]
        return tcs

    @staticmethod
    def read_triangles( f, header ):
        # seek to the triangles offset
        f.seek( header.offset_tris, os.SEEK_SET )

        # triangles are stored as 3 unsigned shorts for the vertex indices
        # and 3 unsigned shorts for the texture coordinates indices
        triangles = numpy.array(
            MD2_Mesh._load_block( f, '< 6H', header.num_tris ),
            dtype = numpy.uint16
            )
        triangles.shape = (-1, 6)

        # extract the vertex indices and tcs
        vertex_indices = triangles[ : , :3 ]
        tc_indices = triangles[ : , 3: ]

        vertex_indices = vertex_indices.flatten()
        tc_indices = tc_indices.flatten()

        triangles = MD2_Mesh.triangle_layout._make(
            [ vertex_indices, tc_indices ]
            )

        return triangles

    @staticmethod
    def read_frames( f, header ):
        # seek to the frames offset
        f.seek( header.offset_frames, os.SEEK_SET )
        return [ MD2_Mesh.read_frame( f, header ) for x in xrange( header.num_frames ) ]

    @staticmethod
    def read_frame( f, header ):
        # frame scale and translation are 2x3 32 bit floats
        frame_translations = numpy.array(
            MD2_Mesh._load_block( f, '< 3f', 2 ),
            dtype = numpy.float
            )
        # extract the scale and translation vector
        scale = frame_translations[ 0 ]
        translation = frame_translations[ 1 ]

        # read the frame name
        # frame name is a 16 unsigned byte string
        name, = MD2_Mesh._load_block( f, '< 16s', 1 )[0]
        # remove any \x00 characters as they confuse python
        name = name.strip( '\x00' )

        # frame has 3 unsigned bytes for the vertex coordinates
        # and 1 unsigned byte for the normal index
        frame_vertex_data = numpy.array(
            MD2_Mesh._load_block( f, '<4B', header.num_vertices ),
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

        # extract the normal values
        normal_indices = frame_vertex_data[ :, 3 ]
        # convert from normal indice to normal vector
        normals = MD2_Mesh.normal_lookup_table[ normal_indices ]
        normals.shape = (-1, 3)

        return MD2_Mesh.frame_layout._make(
            [ name, vertices, normals ]
            )

    @staticmethod
    def convert_indicies_for_all_frames( frames, triangles ):
        return [ MD2_Mesh.convert_indices_for_frame( frame, triangles ) for frame in frames ]

    @staticmethod
    def convert_indices_for_frame( frame, triangles ):
        return MD2_Mesh.frame_layout._make(
            [
                frame.name,
                frame.vertices[ triangles.vertex_indices ],
                frame.normals[ triangles.vertex_indices ]
                ]
            )

    def render_frame( self, frame ):
        # split the frame time into whole and fractional parts
        # the whole part is the current frame
        # the fractional part is the % through the frame
        delta, current_frame = math.modf( frame )
        current_frame = int(current_frame)

        # using the vertices for this frame, pull out the
        # vertices in order of our triangles
        # do the same for the normals
        vertices = self.frames[ current_frame ].vertices
        normals = self.frames[ current_frame ].normals

        # interpolate between this frame and the next
        # only do this is the time is not 0.0
        # and we're not at the end of the list
        if delta > 0.0:
            next_vertices = self.frames[ current_frame + 1 ].vertices
            next_normals = self.frames[ current_frame + 1 ].normals

            # scale the difference based on the time
            vertices = vector.interpolate( vertices, next_vertices, delta )
            normals = vector.interpolate( normals, next_normals, delta )

            # ensure our normals are vector length
            vector.normalise( normals )

        # pass to opengl
        pyglet.graphics.draw(
            vertices.size / 3,
            GL_TRIANGLES,
            ('v3f/static', vertices.flatten()),
            ('n3f/static', normals.flatten()),
            ('t2f/static', self.tcs.flatten())
            )

    def render( self ):
        self.render_frame( self.frame )

    def render_tcs( self, origin, size ):
        x = origin[ 0 ]
        y = origin[ 1 ]
        width = size[ 0 ]
        height = size[ 1 ]

        glPushAttrib( GL_ALL_ATTRIB_BITS )

        # we want to draw just the lines of the triangles
        # so change our polymode to line only
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        # draw an ourline of the texture
        glBegin( GL_QUADS )
        glVertex2f( 0.0 + x, 0.0 + y )
        glVertex2f( 0.0 + x, height + y )
        glVertex2f( width + x, height + y )
        glVertex2f( width + x, 0.0 + y )
        glEnd()

        # find the TCs for each triangle
        tcs_triangles = numpy.array( self.tcs )
        tcs_triangles *= size
        tcs_triangles += origin

        # pass to opengl
        pyglet.graphics.draw(
            len( tcs_triangles ),
            GL_TRIANGLES,
            ('v2f/static', tcs_triangles.flatten())
            )

        glPopAttrib()
    
