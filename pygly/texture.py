"""
http://www.opengl.org/sdk/docs/man3/
http://www.opengl.org/sdk/docs/man/xhtml/glBindTexture.xml
http://www.opengl.org/sdk/docs/man3/xhtml/glBindTexture.xml
http://www.opengl.org/sdk/docs/man/xhtml/glTexImage2D.xml
http://www.opengl.org/sdk/docs/man3/xhtml/glTexImage2D.xml
http://www.opengl.org/sdk/docs/man/xhtml/glTexParameter.xml
http://www.opengl.org/sdk/docs/man3/xhtml/glTexParameter.xml
"""

import numpy
from pygly.gl import *
from PIL import Image
from ctypes import *

from collections import namedtuple


def opengl_enum_to_type( enum ):
    """Converts an OpenGL type enumeration
    into an actual OpenGL data type.
    """
    return {
        GL_BYTE:            GLbyte,
        GL_UNSIGNED_BYTE:   GLubyte,
        GL_SHORT:           GLshort,
        GL_UNSIGNED_SHORT:  GLushort,
        GL_INT:             GLint,
        GL_UNSIGNED_INT:    GLuint,
        GL_FLOAT:           GLfloat,
        GL_DOUBLE:          GLdouble,
        }[ enum ]

def set_properties( target, properties ):
    """Convenience function that calls any array of
    specified functions with the specified data.

    Target is the texture target type.
    Eg. GL_TEXTURE_2D.

    Properties is a list of triples.
    The format of these is:
        function, parameter, value

    The purpose of this function is to call
    glTexParameteri, glTexParameterf,
    glTexParameterfv, glTexParameteriv, glTexParameterIiv,
    and glTexParameterIuiv.

    This is used by some functions because it is more
    efficient to call this before loading the texture
    data, but after texture creation.

    The most common reason for this is to pass
    (at the least) the minification and magnification
    parameters during texture creation.

    For example:
    set_properties(
        GL_TEXTURE_2D,
        [
            (glTexParameteri, GL_TEXTURE_MIN_FILTER, GL_LINEAR),
            (glTexParameteri, GL_TEXTURE_MAX_FILTER, GL_LINEAR),
            ]
        )

    A list of OpenGL functions and properties can
    be found here:
    http://www.opengl.org/sdk/docs/man/xhtml/glTexParameter.xml
    http://www.opengl.org/sdk/docs/man3/xhtml/glTexParameter.xml
    """
    for function, property, values in properties:
        if type(values) is not list:
            values = list([values])
        function( target, property, *values )


class ArrayTexture( object ):

    def __init__( self, data ):
        super( ArrayTexture, self ).__init__()

        # store the data as a numpy array
        self.data = numpy.array( data )

    def create_texture_2d(
        self,
        target = GL_TEXTURE_2D,
        properties = None,
        level = 0,
        border = False,
        internal_format = None,
        format = None,
        swizzle = None
        ):
        """Uses the loaded PIL image to create
        a 2D texture.
        This creates a texture using the
        set_texture_2D method but creates the
        texture and binds and unbinds it for you.

        This will create a new texture each time
        this function is called.
        """
        # create the texture
        texture = Texture( target )
        texture.bind()

        # set our texture data
        self.set_texture_2d(
            target,
            properties,
            level,
            border,
            internal_format,
            format,
            swizzle
            )

        # unbind
        texture.unbind()

        return texture

    def set_texture_2d(
        self,
        target = GL_TEXTURE_2D,
        properties = None,
        level = 0,
        border = False,
        internal_format = None,
        format = None,
        swizzle = None
        ):
        """Sets the data of the currently bound
        texture to this image.
        This calls glTexImage2D.

        data: The texture data to load as a list or numpy array.
            The shape of the data will determine if
            it is treated as a 1d, 2d or 3d array.
            The data must have a shape of either,
            1, 2 or 3 dimensions.
        level: Specifies the mip level the data is being set for.
        border: Specifies if the texture is to use a border.

        target: Specifies the image target type.
            Valid values are:
            GL_TEXTURE_2D,
            GL_PROXY_TEXTURE_2D,
            GL_TEXTURE_1D_ARRAY,
            GL_PROXY_TEXTURE_1D_ARRAY,
            GL_TEXTURE_RECTANGLE,
            GL_PROXY_TEXTURE_RECTANGLE,
            GL_TEXTURE_CUBE_MAP_POSITIVE_X,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
            GL_PROXY_TEXTURE_CUBE_MAP

        internal_format: Specifies the format the data
            is stored in.
            Leave as None to auto-detect.
            Auto detection will specify the following
            depending on the number of
            channels:
            1: GL_RED,
            2: GL_RG,
            3: GL_RGB,
            4: GL_RGBA.
            If the detected type is GL_FLOAT,
            the auto-detection will change to the following:
            1: GL_RED32F,
            2: GL_R32F,
            3: GL_RBG32F,
            4: GL_RGBA32F.

        format: The format the is to be used for.
            This must correlate to both the type,
            and internal format.
            This is usually GL_RGB or GL_RGBA.
            Leave as None to auto-detect.
            Auto detection will specify the following
            depending on the number of channels:
            1: GL_RED,
            3: GL_RGB,
            4: GL_RGBA.
        type: Specifies the data type used.
            This must correlate to both the format
            and internal format.
            Leave as None to auto-detect.
            Auto detection will specify the following
            depending on the data type:
            uint8:      GL_UNSIGNED_BYTE
            int8:       GL_BYTE
            uint16:     GL_UNSIGNED_SHORT
            int16:      GL_SHORT
            uint32:     GL_UNSIGNED_INT
            int32:      GL_INT
            float32:    GL_FLOAT
            float64:    GL_DOUBLE
        """
        # set our opengl texture properties
        # we do this now so the driver can convert the
        # data as it loads, rather than afterwards.
        set_properties( target, properties )

        # determine our texture type first
        # we use this later in the loading process
        #_type_enum = type if type else ArrayTexture.numpy_to_type( self.data )
        _type_enum = ArrayTexture.numpy_to_type( self.data )

        _type_obj = opengl_enum_to_type( _type_enum )

        _internal_format = internal_format if internal_format else ArrayTexture.numpy_to_internal_format( self.data, _type_enum )

        _format = format if format else ArrayTexture.numpy_to_format( self.data )

        _border = 0 if not border else 1

        if swizzle != None:
            # set our texture swizzle if one was passed
            swizzle = (GLint * 4)(*swizzle)
            glTexParameteriv(
                target,
                GL_TEXTURE_SWIZZLE_RGBA,
                swizzle
                )

        # construct our function args
        # the only difference between glTexImage1D/2D/3D
        # is the addition of extra size dimensions
        # we will dynamically add these to the middle
        # of the parameter list
        glTexImage2D(
            target,
            level,
            _internal_format,
            self.data.shape[ 0 ],
            self.data.shape[ 1 ],
            _border,
            _format,
            _type_enum,
            (_type_obj * self.data.size)(*self.data.flat)
            )

    @staticmethod
    def numpy_to_internal_format( data, type ):
        if type == GL_FLOAT:
            # check if we've got float textures
            return {
                1:  GL_RED32F,
                2:  GL_RG32F,
                3:  GL_RGB32F,
                4:  GL_RGBA32F,
                }[ data.shape[ -1 ] ]
        elif type == GL_HALF_FLOAT:
            return {
                1:  GL_RED16F,
                2:  GL_RG16F,
                3:  GL_RGB16F,
                4:  GL_RGBA16F,
                }[ data.shape[ -1 ] ]
        else:
            # standard textures
            return {
                1:  GL_RED,
                2:  GL_RG,
                3:  GL_RGB,
                4:  GL_RGBA,
                }[ data.shape[ -1 ] ]

    @staticmethod
    def numpy_to_format( data ):
        return {
            1:  GL_RED,
            2:  GL_RG,
            3:  GL_RGB,
            4:  GL_RGBA,
            }[ data.shape[ -1 ] ]

    @staticmethod
    def numpy_to_type( data ):
        return {
            numpy.dtype('int8'):    GL_BYTE,
            numpy.dtype('uint8'):   GL_UNSIGNED_BYTE,
            numpy.dtype('int16'):   GL_SHORT,
            numpy.dtype('uint16'):  GL_UNSIGNED_SHORT,
            numpy.dtype('int32'):   GL_INT,
            numpy.dtype('uint32'):  GL_UNSIGNED_INT,
            numpy.dtype('float32'): GL_FLOAT,
            #numpy.dtype('float64'): GL_DOUBLE,
            numpy.dtype('float64'): GL_FLOAT,
            }[ data.dtype ]


class PIL_Texture( object ):
    
    def __init__( self, image ):
        super( PIL_Texture, self ).__init__()

        self.image = image

        # some TIFF images don't render correctly
        # if we convert them to RGBX they suddenly
        # begin rendering correctly
        # so let's do that
        # some TIFF images can't be converted
        # this may throw an IOError exception
        if self.image.format == 'TIFF':
            self.image = self.image.convert('RGBX')

        # handle unsupported formats
        if \
            self.image.mode == 'P' or \
            self.image.mode == 'CMYK' or \
            self.image.mode == 'YCbCr':
            # handle unsupported texture formats
            # convert from unsupported formats to RGBX
            self.image = self.image.convert('RGBX')

        # flip the image
        # PIL loads images upside down to OpenGL
        self.image = self.image.transpose(
            Image.FLIP_TOP_BOTTOM
            )

    def setup_swizzle( self, target ):
        """Sets up some OpenGL state for the image
        that is required to load correctly.
        This is called after the texture is bound
        but before the data is loaded.
        """
        # some formats need conversion or
        # special opengl parameters to load correctly
        if \
            self.image.mode == 'L' or \
            self.image.mode == 'I' or \
            self.image.mode == 'F':
            # GL_LUMINANCE is deprecated
            # we need to provide a swizzle to
            # tell OpenGL how to read the data
            # http://stackoverflow.com/questions/9355869/invalid-enumerant-when-creating-16-bit-texture
            # http://www.opengl.org/wiki/Texture#Swizzle_mask
            # luminance uses the one value for all
            # RGB channels and 1.0 for alpha.
            swizzle = (GLint * 4)(GL_RED, GL_RED, GL_RED, GL_ONE)
            glTexParameteriv(
                target,
                GL_TEXTURE_SWIZZLE_RGBA,
                swizzle
                )
        elif self.image.mode == 'LA':
            # GL_LUMINANCE_ALPHA is also deprecated
            # perform a swizzle, but preserve the alpha value
            # luminance Alpha uses the first value for all
            # RGB channels and the second for the alpha.
            swizzle = (GLint * 4)(GL_RED, GL_RED, GL_RED, GL_GREEN)
            glTexParameteriv(
                target,
                GL_TEXTURE_SWIZZLE_RGBA,
                swizzle
                )

    @property
    def opengl_enums( self ):
        """Returns the OpenGL enumerations for the
        PIL image mode.
        """
        mode = self.image.mode

        # treat RGBX and RGBa as RGBA
        if mode == 'RGBX' or mode == 'RGBa':
            mode = 'RGBA'

        return {
            'RGB':  (
                GL_UNSIGNED_BYTE,       # type
                GL_RGB,                 # format
                GL_RGB8,                # internal format
                ),
            'RGBA': (
                GL_UNSIGNED_BYTE,       # type
                GL_RGBA,                # format
                GL_RGBA8,               # internal format
                ),
            'L':    (
                GL_UNSIGNED_BYTE,       # type
                GL_RED,                 # format
                GL_RGBA,                # internal format
                ),
            'LA':   (
                GL_UNSIGNED_BYTE,       # type
                GL_RG,                  # format
                GL_RGBA,                # internal format
                ),
            'F':    (
                GL_FLOAT,               # type
                GL_RGB,                 # format
                GL_RGB32F,              # internal format
                ),
            'I':    (
                GL_INT,                 # type
                GL_RGB,                 # format
                GL_RGB32I,              # internal format
                ),
            }[ mode ]

    def create_texture_2d(
        self,
        target = GL_TEXTURE_2D,
        properties = None,
        level = 0,
        border = False
        ):
        """Uses the loaded PIL image to create
        a 2D texture.
        This creates a texture using the
        set_texture_2D method but creates the
        texture and binds and unbinds it for you.

        This will create a new texture each time
        this function is called.
        """
        # create the texture
        texture = Texture( target )
        texture.bind()

        # set our texture data
        self.set_texture_2d( target, properties, level, border )

        # unbind
        texture.unbind()

        return texture

    def set_texture_2d(
        self,
        target = GL_TEXTURE_2D,
        properties = None,
        level = 0,
        border = False
        ):
        """Sets the data of the currently bound
        texture to this image.
        This calls glTexImage2D.
        """
        # set our opengl texture properties
        # we do this now so the driver can convert the
        # data as it loads, rather than afterwards.
        set_properties( target, properties )

        # determine what type of texture we're loading
        _type, _format, _internal_format = self.opengl_enums
        _type_obj = opengl_enum_to_type( _type )
        _border = 0 if not border else 1

        # perform any opengl conversion that we need
        # for this image format
        self.setup_swizzle( target )

        # set data
        glTexImage2D(
            target,
            level,
            _internal_format,
            self.image.size[ 0 ],
            self.image.size[ 1 ],
            _border,
            _format,
            _type,
            self.image.tostring()
            )


class Texture( object ):
    """Provides a convenience wrapper around
    the glGenTexture and glBindTexture functions.

    You __MUST__ set the GL_TEXTURE_MAG_FILTER
    and GL_TEXTURE_MIN_FILTER parameters or the
    texture will NOT render!
    It is recommended, for performance reasons, to
    set any texture properties before loading the data
    so the driver doesn't have to re-format data
    after loading.
    """

    def __init__( self, target ):
        """Creates a Texture object of the
        specified type.

        This class will call glGenTextures and
        create a texture ID which is accessible
        through the 'texture' property.

        The texture will be freed when this
        object is deleted.
        """
        super( Texture, self ).__init__()

        self.target = target

        self.texture = (GLuint)()
        glGenTextures( 1, self.texture )

    def __del__( self ):
        # free our texture
        texture = getattr( self, 'texture', None )
        if texture and texture.value != 0:
            glDeleteTextures( 1, texture )

    def bind( self ):
        glBindTexture( self.target, self.texture )

    def unbind( self ):
        glBindTexture( self.target, 0 )


