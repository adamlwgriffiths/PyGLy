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


def set_swizzle( target, swizzle ):
    gl_swizzle = (GLint * 4)(*swizzle)
    glTexParameteriv(
        target,
        GL_TEXTURE_SWIZZLE_RGBA,
        gl_swizzle
        )

def set_min_mag_filter( target, min, mag ):
    glTexParameteri(
        target,
        GL_TEXTURE_MIN_FILTER,
        min
        )
    glTexParameteri(
        target,
        GL_TEXTURE_MAG_FILTER,
        mag
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

    def set_swizzle( self, swizzle ):
        set_swizzle( self.target, swizzle )

    def set_min_mag_filter( self, min, mag ):
        set_min_mag_filter( self.target, min, mag )



def _opengl_enum_to_type( enum ):
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


def set_raw_texture(
    func,
    data,
    target,
    format = None,
    internal_format = None,
    level = 0,
    border = False,
    ):
    """Sets the data of the currently bound
    texture to this image.
    This calls glTexImage1D.

    The parameters are the same as in the set_raw_texture_2d
    function.
    """
    def numpy_to_internal_format( data, type ):
        if type == GL_FLOAT:
            # check if we've got float textures
            return {
                1:  GL_R32F,
                2:  GL_RG32F,
                3:  GL_RGB32F,
                4:  GL_RGBA32F,
                }[ data.shape[ -1 ] ]
        elif type == GL_HALF_FLOAT:
            return {
                1:  GL_R16F,
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

    def numpy_to_format( data ):
        return {
            1:  GL_RED,
            2:  GL_RG,
            3:  GL_RGB,
            4:  GL_RGBA,
            }[ data.shape[ -1 ] ]

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

    np_data = numpy.array( data )

    # determine our texture type first
    # we use this later in the loading process
    gl_enum = numpy_to_type( np_data )
    gl_type = _opengl_enum_to_type( gl_enum )
    gl_internal_format = internal_format if internal_format else numpy_to_internal_format( np_data, gl_enum )
    gl_format = format if format else numpy_to_format( np_data )
    gl_border = 0 if not border else 1

    # get our texture dimensions
    # ignore the last dimension, this is the
    # number of channels
    size = np_data.shape[:-1]

    # construct our function args
    # the only difference between glTexImage1D/2D/3D
    # is the addition of extra size dimensions
    # we will dynamically add these to the middle
    # of the parameter list
    params = [
        target,
        level,
        gl_internal_format
        ] + \
        list(size) + [
        gl_border,
        gl_format,
        gl_enum,
        (gl_type * np_data.size)(*np_data.flat)
        ]

    func( *params )


def set_raw_texture_1d(
    data,
    target = GL_TEXTURE_1D,
    format = None,
    internal_format = None,
    level = 0,
    border = False,
    ):
    """Sets the data of the currently bound
    texture to this image.
    This calls glTexImage1D.

    The parameters are the same as in the set_raw_texture_2d
    function.
    """
    set_raw_texture(
        glTexImage1D,
        data,
        target,
        format,
        internal_format,
        level,
        border
        )

def set_raw_texture_2d(
    data,
    target = GL_TEXTURE_2D,
    format = None,
    internal_format = None,
    level = 0,
    border = False,
    ):
    """Sets the data of the currently bound
    texture to this image.
    This calls glTexImage2D.

    data: The texture data to load as a list or numpy array.
        The shape of the array is important.
        If format auto-detection is used, it is important
        that the last dimension is the size of the number
        of channels.
        Ie, for a luminance texture, do not send an array
        of shape (32,32).
        Instead, send an array of shape (32,32,1)
    target: Specifies the image target type.
    level: Specifies the mip level the data is being set for.
    border: Specifies if the texture is to use a border.
    """
    set_raw_texture(
        glTexImage2D,
        data,
        target,
        format,
        internal_format,
        level,
        border
        )



def set_pil_texture_2d(
    image,
    target = GL_TEXTURE_2D,
    level = 0,
    border = False
    ):
    """Sets the data of the currently bound
    texture to this image.
    This calls glTexImage2D.
    """
    # some TIFF images don't render correctly
    # if we convert them to RGBX they suddenly
    # begin rendering correctly
    # so let's do that
    # some TIFF images can't be converted
    # this may throw an IOError exception
    if image.format == 'TIFF':
        image = image.convert('RGBX')

    # handle unsupported formats
    if \
        image.mode == 'P' or \
        image.mode == 'CMYK' or \
        image.mode == 'YCbCr':
        # convert from unsupported formats to RGBX
        image = image.convert('RGBX')

    # flip the image
    # PIL loads images upside down to OpenGL
    image = image.transpose(
        Image.FLIP_TOP_BOTTOM
        )

    # determine what type of texture we're loading
    gl_enum, gl_format, gl_internal_format = _pil_enums( image )
    gl_type = _opengl_enum_to_type( gl_enum )
    gl_border = 0 if not border else 1

    # perform any opengl conversion that we need
    # for this image format
    _pil_swizzle( target, image )

    # set data
    glTexImage2D(
        target,
        level,
        gl_internal_format,
        image.size[ 0 ],
        image.size[ 1 ],
        gl_border,
        gl_format,
        gl_enum,
        image.tostring()
        )

def _pil_swizzle( target, image ):
    """Sets up some OpenGL state for the image
    that is required to load correctly.
    This is called after the texture is bound
    but before the data is loaded.
    """
    # some formats need conversion or
    # special opengl parameters to load correctly
    if \
        image.mode == 'L' or \
        image.mode == 'I' or \
        image.mode == 'F':
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
    elif image.mode == 'LA':
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

def _pil_enums( image ):
    """Returns the OpenGL enumerations for the
    PIL image mode.
    """
    mode = image.mode

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

