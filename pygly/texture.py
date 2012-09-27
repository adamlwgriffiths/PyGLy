"""
http://www.opengl.org/sdk/docs/man/xhtml/glBindTexture.xml
http://www.opengl.org/sdk/docs/man/xhtml/glTexImage2D.xml
http://www.opengl.org/sdk/docs/man/xhtml/glTexParameter.xml
"""

import numpy
from pygly.gl import *
from PIL import Image

from collections import namedtuple


class Texture( object ):
    """
    Once the texture object is created, data must
    be loaded into it.
    There are a number of data loading methods to
    suit your needs.

    Once data is loaded, you __MUST__ set the
    GL_TEXTURE_MAG_FILTER and GL_TEXTURE_MIN_FILTER
    parameters or the texture will NOT render!
    Wrappers for this are not provided.
    Simple bind the texture and call the appopriate
    GL functions.

    Ie:
    data = numpy.random.random_integers( 120, 255, (32,32,3) )
    texture = Texture()
    texture.data( data.astype('uint8') )
    texture.bind()
    glTexParameteri(            texture.target,
        GL_TEXTURE_MIN_FILTER,
        GL_LINEAR
        )
    glTexParameteri(            texture.target,
        GL_TEXTURE_MAG_FILTER,
        GL_LINEAR
        )
    texture.unbind()
    """

    def __init__( self ):
        """If you wish to bind the texture prior to loading
        and data, you MUST set texture.target to an
        appropriate value as it is required for the bind call.
        texture.target is the 'target' parameter passed to the
        'glBindTexture( target, id )' function.
        """
        super( Texture, self ).__init__()

        self.size = None
        self.unit = GL_TEXTURE0
        self.target = None

        self.texture = (GLuint)()
        glGenTextures( 1, self.texture )

    def __del__( self ):
        # free our texture
        texture = getattr( self, 'texture', None )
        if texture and texture.value != 0:
            glDeleteTextures( 1, texture )

    def bind( self ):
        glActiveTexture( self.unit )
        glBindTexture( self.target, self.texture )

    def unbind( self ):
        glActiveTexture( self.unit )
        glBindTexture( self.target, 0 )

    def pil_data_convert( self, image, level = 0, border = 0, format = None ):
        """Sets the data for the currently bound texture using a PIL image.
        The PIL data is converted to the specified format.
        """
        channels = {
            GL_COLOR_INDEX:     1,
            GL_RED:             1,
            GL_GREEN:           1,
            GL_BLUE:            1,
            GL_ALPHA:           1,
            GL_RGB:             3,
            GL_BGR:             3,
            GL_RGBA:            4,
            GL_BGRA:            4,
            GL_LUMINANCE:       1,
            GL_LUMINANCE_ALPHA: 2,
            }
        mode = {
            GL_COLOR_INDEX:     None,
            GL_RED:             None,
            GL_GREEN:           None,
            GL_BLUE:            None,
            GL_ALPHA:           None,
            GL_RGB:             'RGB',
            GL_BGR:             'RGB',
            GL_RGBA:            'RGBA',
            GL_BGRA:            'RGBA',
            GL_LUMINANCE:       'L',
            GL_LUMINANCE_ALPHA: 'LA',
            }[ format ]

        # ensure we have enough data for this format
        if channels != image.bands:
            # check if we're just adding an alpha component
            if channels == 4 and image.bands == 3:
                # just add an alpha
                mode = 'RGBX'
            else:
                raise ValueError( 'Image format incompatible with requested format' )

        # convert the image
        image = image.convert( mode )

        # extract the data
        data = image.tostring()

        # manipulate the channels if required
        if format == GL_BGR:
            data.shape = (-1,4)
            data[:,] = data[:,-1]
        elif format == GL_BGRA:
            data.shape = (-1,4)
            data[:,:3] = data[:,3:0]

        # TODO:

    def pil_data( self, image, level = 0, border = 0 ):
        """Sets the data for the currently bound texture using a PIL image.
        The data types are set based on the PIL format.
        """
        """
        http://www.pythonware.com/library/pil/handbook/image.htm
        http://www.pythonware.com/library/pil/handbook/concepts.htm

        1 (1-bit pixels, black and white, stored with one pixel per byte)
        L (8-bit pixels, black and white)
        P (8-bit pixels, mapped to any other mode using a colour palette)
        RGB (3x8-bit pixels, true colour)
        RGBA (4x8-bit pixels, true colour with transparency mask)
        CMYK (4x8-bit pixels, colour separation)
        YCbCr (3x8-bit pixels, colour video format)
        I (32-bit signed integer pixels)
        F (32-bit floating point pixels)
        """
        mode = image.mode
        pass

    def data(
        self,
        data,
        level = 0,
        border = False,
        target = None,
        internal_format = None,
        format = None,
        type = None
        ):
        """Sets the data for the currently bound texture.

        data: The texture data to load as a list or numpy array.
            The shape of the data will determine if it is treated as a
            1d, 2d or 3d array.
            The data must have a shape of either, 1, 2 or 3 dimensions.
        level: Specifies the mip level the data is being set for.
        border: Specifies if the texture is to use a border.
        internal_format: Specifies the format the data is stored in.
            Leave as None to auto-detect.
            Valid values are:
            GL_ALPHA, GL_ALPHA4, GL_ALPHA8, GL_ALPHA12, GL_ALPHA16,
            GL_COMPRESSED_ALPHA, GL_COMPRESSED_LUMINANCE,
            GL_COMPRESSED_LUMINANCE_ALPHA, GL_COMPRESSED_INTENSITY,
            GL_COMPRESSED_RGB, GL_COMPRESSED_RGBA, GL_DEPTH_COMPONENT,
            GL_DEPTH_COMPONENT16, GL_DEPTH_COMPONENT24,
            GL_DEPTH_COMPONENT32, GL_LUMINANCE, GL_LUMINANCE4,
            GL_LUMINANCE8, GL_LUMINANCE12, GL_LUMINANCE16,
            GL_LUMINANCE_ALPHA, GL_LUMINANCE4_ALPHA4,
            GL_LUMINANCE6_ALPHA2, GL_LUMINANCE8_ALPHA8,
            GL_LUMINANCE12_ALPHA4, GL_LUMINANCE12_ALPHA12,
            GL_LUMINANCE16_ALPHA16, GL_INTENSITY, GL_INTENSITY4,
            GL_INTENSITY8, GL_INTENSITY12, GL_INTENSITY16, GL_R3_G3_B2,
            GL_RGB, GL_RGB4, GL_RGB5, GL_RGB8, GL_RGB10, GL_RGB12,
            GL_RGB16, GL_RGBA, GL_RGBA2, GL_RGBA4, GL_RGB5_A1, GL_RGBA8,
            GL_RGB10_A2, GL_RGBA12, GL_RGBA16, GL_SLUMINANCE, GL_SLUMINANCE8,
            GL_SLUMINANCE_ALPHA, GL_SLUMINANCE8_ALPHA8, GL_SRGB, GL_SRGB8,
            GL_SRGB_ALPHA, GL_SRGB8_ALPHA8.
            Leave as None to auto-detect.
            Auto detection will specify the following depending on the number of
            channels:
            1: GL_RED,
            3: GL_RGB,
            4: GL_RGBA.
            If the specified type is GL_HALF_FLOAT, the auto-detection will change to
            the following:
            1: GL_REDF16,
            3: GL_RBGF16,
            4: GL_RGBAF16.
            If the specified type is GL_FLOAT, the auto-detection will change to
            the following:
            1: GL_REDF32,
            3: GL_RBGF32,
            4: GL_RGBAF32.
        format: The format the is to be used for. This must correlate to
            both the type, and internal format.
            This is usually GL_RGB or GL_RGBA.
            Valid values are:
            GL_COLOR_INDEX, GL_RED, GL_GREEN, GL_BLUE, GL_ALPHA, GL_RGB, GL_BGR,
            GL_RGBA, GL_BGRA, GL_LUMINANCE, GL_LUMINANCE_ALPHA.
            Leave as None to auto-detect.
            Auto detection will specify the following depending on the number of
            channels:
            1: GL_RED,
            3: GL_RGB,
            4: GL_RGBA.
        type: Specifies the data type used.
            This must correlate to both the format and internal format.
            Valid values are:
            GL_UNSIGNED_BYTE, GL_BYTE, GL_BITMAP, GL_UNSIGNED_SHORT, GL_SHORT,
            GL_UNSIGNED_INT, GL_INT, GL_FLOAT, GL_UNSIGNED_BYTE_3_3_2,
            GL_UNSIGNED_BYTE_2_3_3_REV, GL_UNSIGNED_SHORT_5_6_5,
            GL_UNSIGNED_SHORT_5_6_5_REV, GL_UNSIGNED_SHORT_4_4_4_4,
            GL_UNSIGNED_SHORT_4_4_4_4_REV, GL_UNSIGNED_SHORT_5_5_5_1,
            GL_UNSIGNED_SHORT_1_5_5_5_REV, GL_UNSIGNED_INT_8_8_8_8,
            GL_UNSIGNED_INT_8_8_8_8_REV, GL_UNSIGNED_INT_10_10_10_2,
            GL_UNSIGNED_INT_2_10_10_10_REV.
            Leave as None to auto-detect.
            Auto detection will specify the following depending on the data type:
            uint8:
            int8:
            uint16:
            int16:
            uint32:
            int32:
            float32:    GL_FLOAT
            float64:
        """
        np_data = numpy.array( data )

        # determine what target we need
        _target = target if target else numpy_to_target( np_data )

        glActiveTexture( self.unit )
        glBindTexture( _target, self.texture )

        # determine which texture type were setting
        # we determine this based on the number of dimensions
        # this must match self.target set in the constructor.
        # we need to take into account that the
        # final dimension is the colours
        func = {
            1:  glTexImage1D,
            2:  glTexImage2D,
            3:  glTexImage3D,
            }[ np_data.ndim - 1 ]

        # determine our texture type first
        # we use this later in the loading process
        _type = type if type else numpy_to_type( np_data )
        _type_enum, _type_obj = _type[ 0 ], _type[ 1 ]

        _internal_format = internal_format if internal_format else numpy_to_internal_format( np_data, _type_enum )
        _format = format if format else numpy_to_format( np_data )
        _border = 0 if not border else 1
        _size = list(np_data.shape)[:-1]

        # construct our function args
        # the only difference between glTexImage1D/2D/3D
        # is the addition of extra size dimensions
        # we will dynamically add these to the middle
        # of the parameter list
        params = [
            _target,
            level,
            _internal_format ] + \
            _size + [ \
            _border,
            _format,
            _type_enum,
            (_type_obj * np_data.size)(*np_data.flat)
            ]

        # call opengl to set our data
        func( *params )

        # store our data
        self.target = _target
        self.size = np_data.shape[ :-1 ]

        glActiveTexture( self.unit )
        glBindTexture( _target, 0 )

def numpy_to_target( data ):
    # we need to take into account that the
    # final dimension is the colours
    return {
        1:  GL_TEXTURE_1D,
        2:  GL_TEXTURE_2D,
        3:  GL_TEXTURE_3D,
        }[ data.shape[ -1 ] - 1 ]

def numpy_to_internal_format( data, type ):
    if type == GL_FLOAT:
        # check if we've got float textures
        return {
            1:  GL_REDF32,
            3:  GL_RGBF32,
            4:  GL_RGBAF32,
            }[ data.shape[ -1 ] ]
    elif type == GL_HALF_FLOAT:
        return {
            1:  GL_REDF16,
            3:  GL_RGBF16,
            4:  GL_RGBAF16,
            }[ data.shape[ -1 ] ]
    else:
        # standard textures
        return {
            1:  GL_RED,
            3:  GL_RGB,
            4:  GL_RGBA,
            }[ data.shape[ -1 ] ]

def numpy_to_format( data ):
    return {
        1:  GL_RED,
        3:  GL_RGB,
        4:  GL_RGBA,
        }[ data.shape[ -1 ] ]

def numpy_to_type( data ):
    return {
        numpy.dtype('int8'):    (GL_BYTE, GLbyte),
        numpy.dtype('uint8'):   (GL_UNSIGNED_BYTE, GLubyte),
        numpy.dtype('int16'):   (GL_SHORT, GLshort),
        numpy.dtype('uint16'):  (GL_UNSIGNED_SHORT, GLushort),
        numpy.dtype('int32'):   (GL_INT, GLint),
        numpy.dtype('uint32'):  (GL_UNSIGNED_INT, GLuint),
        numpy.dtype('float32'): (GL_FLOAT, GLfloat),
        numpy.dtype('float64'): (GL_DOUBLE, GLdouble),
        }[ data.dtype ]



"""

    @classmethod
    def create( cls, data, width, height, format = GL_RGBA ):
        pass

    @classmethod
    def open( cls, filename, format = GL_RGBA ):
        # open the file
        im = Image.open( filename )
        width, height = im.size
        # convert to the requested format
        #im.convert( pil_format )
        return cls.create( im.tostring(), width, height, format )








class Texture2D( Texture ):

    def __init__( self ):
        super( Texture2D, self ).__init__( GL_TEXTURE_2D )

    @property
    def width( self ):
        if not self.dimensions:
            return None
        return self.dimensions[ 0 ]

    @property
    def height( self ):
        if not self.dimensions:
            return None
        return self.dimensions[ 1 ]

    def set_data( self, data, width, height, level = 0, border = False ):
        with self:
            glTexImage2D(
                self.target,        # texture type
                level,              # mip level
                pass,               # internal data format
                width,              # width
                height,             # height
                0 if border == False else 1,    # border
                pass,               # format (channel format)
                pass,               # type (data type)
                data                # data
                )

            # store the dimensions
            self.dimensions = (width, height)




    Type = namedtuple(
        'types',
        [
            'type',
            'enum',
            ]
        )

    InternalFormat = namedtuple(
        'internal_format',
        [
            ],
        )

    Format = namedtuple(
        'internal_format',
        [
            ],
        )

    types = {
        'byte':     Type( GLubyte, GL_UNSIGNED_BYTE ),
        'short':    Type( GLushort, GL_UNSIGNED_SHORT ),
        'float':    Type( GLfloat, GL_FLOAT ),
        }

    internal_formats = {
        1:          GL_RED,
        2:          GL_RG,
        3:          GL_RGB,
        4:          GL_RGBA,
        'rgb':      GL_RGB,
        'rgba':     GL_RGBA,
        }

    formats = {
        #GL_COLOR_INDEX,
        GL_RED,
        GL_GREEN,
        GL_BLUE,
        GL_ALPHA,
        GL_RGB,
        GL_BGR,
        GL_RGBA,
        GL_BGRA,
        GL_LUMINANCE,
        GL_LUMINANCE_ALPHA,
        }

"""
