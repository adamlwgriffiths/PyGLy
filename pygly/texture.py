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
from ctypes import *

import pygly.utils


def create_texture( target ):
    texture = (GLuint)()
    glGenTextures( 1, texture )

    return texture

def active_texture( unit ):
    glActiveTexture( GL_TEXTURE0 + unit )

def bind( texture ):
    glBindTexture( texture[ 0 ], texture[ 1 ] )

def unbind( texture ):
    glBindTexture( texture[ 0 ], 0 )

def bind_to_unit( unit, texture ):
    active_texture( unit )
    bind( texture )

def unbind_from_unit( unit, texture ):
    active_texture( unit )
    unbind( texture )

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

def set_wrap_mode( target, wrap_s, wrap_t ):
    glTexParameteri(
        target,
        GL_TEXTURE_WRAP_S,
        wrap_s
        )
    glTexParameteri(
        target,
        GL_TEXTURE_WRAP_T,
        wrap_t
        )

def texture_alignment( size ):
    """Determines a textures byte alignment.

    If the width isn't a power of 2
    we need to adjust the byte alignment of the image.
    The image height is unimportant

    http://www.opengl.org/wiki/Common_Mistakes#Texture_upload_and_pixel_reads
    """

    # extract the texture's width
    # for 1d, this is the first dimension
    # for all others, this is the second
    width = size[ 0 ]
    if len(size) > 1:
        width = size[ 1 ]
        
    # we know the alignment is appropriate
    # if we can divide the width by the
    # alignment cleanly
    # valid alignments are 1,2,4 and 8
    # put 4 first, since it's the default
    alignments = [4,8,2,1]
    for alignment in alignments:
        if width % alignment == 0:
            return alignment


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

    targets = {
        '1d':       GL_TEXTURE_1D,
        '1da':      GL_TEXTURE_1D_ARRAY,
        '2d':       GL_TEXTURE_2D,
        '2da':      GL_TEXTURE_2D_ARRAY,
        '3d':       GL_TEXTURE_3D,
        }

    # http://www.khronos.org/files/opengl-quick-reference-card.pdf
    types = {
        'i8':       (GL_BYTE, GLbyte),
        'u8':       (GL_UNSIGNED_BYTE, GLubyte),
        'i16':      (GL_SHORT, GLshort),
        'u16':      (GL_UNSIGNED_SHORT, GLushort),
        'i32':      (GL_INT, GLint),
        'u32':      (GL_UNSIGNED_INT, GLuint),
        # no native half-float
        'f16':      (GL_HALF_FLOAT, GLfloat),
        'f32':      (GL_FLOAT, GLfloat),
        'f64':      (GL_DOUBLE, GLdouble),
        }

    # http://www.opengl.org/wiki/Image_Formats#Required_formats
    formats = {
        # R
        'r':        GL_RED,
        'r8':       GL_R8,
        'r16':      GL_R16,
        'r16i':     GL_R16I,
        'r32i':     GL_R32I,
        'r16f':     GL_R16F,
        'r32f':     GL_R32F,
        # RG
        'rg':       GL_RG,
        'rg8':      GL_RG8,
        'rg16':     GL_RG16,
        'rg16i':    GL_RG16I,
        'rg32i':    GL_RG32I,
        'rg16f':    GL_RG16F,
        'rg32f':    GL_RG32F,
        # RGB
        'rgb':      GL_RGB,
        'rgb4':     GL_RGB4,
        'rgb8':     GL_RGB8,
        'rgb16':    GL_RGB16,
        'rgb16i':   GL_RGB16I,
        'rgb32i':   GL_RGB32I,
        'rgb16f':   GL_RGB16F,
        'rgb32f':   GL_RGB32F,
        # RGBA
        'rgba':     GL_RGBA,
        'rgba4':    GL_RGBA4,
        'rgba8':    GL_RGBA8,
        'rgba16':   GL_RGBA16,
        'rgba16i':  GL_RGBA16I,
        'rgba32i':  GL_RGBA32I,
        'rgba16f':  GL_RGBA16F,
        'rgba32f':  GL_RGBA32F,
        # SRGB
        'srgb':     GL_SRGB,
        'srgb8':    GL_SRGB8,
        # Specialised
        'rgb10a2':  GL_RGB10_A2,
        'rg11fb10f':    GL_R11F_G11F_B10F,
        'rgb9e5':   GL_RGB9_E5,
        'srgba8':   GL_SRGB8_ALPHA8,
        'd16':      GL_DEPTH_COMPONENT16,
        'd24':      GL_DEPTH_COMPONENT24,
        'd32f':     GL_DEPTH_COMPONENT32F,
        'd24s8':    GL_DEPTH24_STENCIL8,
        'd32fs8':   GL_DEPTH32F_STENCIL8,
        }

    channels = {
        'r':        GL_RED,
        'g':        GL_GREEN,
        'b':        GL_BLUE,
        '1':        GL_ONE,
        '0':        GL_ZERO,
        }

    @staticmethod
    def parse_format( format ):
        """Parse the texture format string.

        The format is as follows:
        type/format/internalformat/swizzle

        The swizzle parameter is optional

        For example:
        'u8/r8/rgba/rrr1'
        This would convert a luminance texture (single channel)
        using uint8 data type (GL_UNSIGNED_BYTE) to an RGBA
        texture using a swizzle with RGB channels receiving the
        'red' value and alpha receiving the constant '1' (rrr1).
        """
        def parse_swizzle( swizzle ):
            if not swizzle:
                return None

            result = []
            for channel in swizzle:
                result.append( Texture.channels[ channel ] )
            return tuple(result)


        # extract the values from the format string
        values = format.split('/')
        type, format, internal_format, swizzle = pygly.utils.extract_tuple( values, 4 )

        return (
            Texture.types[ type ],
            Texture.formats[ format ],
            Texture.formats[ internal_format ],
            parse_swizzle( swizzle )
            )

    def __init__( self, target, image_func, sub_image_func ):
        """Creates a Texture object of the
        specified type.

        This class will call glGenTextures and
        create a texture ID which is accessible
        through the 'texture' property.

        The texture will be freed when this
        object is deleted.
        """
        super( Texture, self ).__init__()

        if type(target) is str:
            global targets
            target = targets[ target ]

        self._image_func = image_func
        self._sub_image_func = sub_image_func

        self.target = target
        self.texture = create_texture( target )

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

    def set_wrap_mode( self, wrap_s, wrap_t ):
        set_wrap_mode( self.target, wrap_s, wrap_t )

    def set_image(
        self,
        data,
        size,
        format,
        level = 0,
        border = False
        ):
        # set the data
        self._texture_func(
            self._image_func,
            data,
            size,
            format,
            level,
            border
            )

    def set_sub_image(
        self,
        data,
        offset,
        size,
        format,
        level = 0,
        border = False
        ):
        # set the data
        self._texture_func(
            self._sub_image_func,
            data,
            [].extend(offset).extend(size),
            format,
            level,
            border
            )

    def _texture_func(
        self,
        func,
        data,
        size,
        format,
        level = 0,
        border = False
        ):
        # parse the format string
        type_tuple, gl_format, gl_internal_format, gl_swizzle = Texture.parse_format( format )

        # extract the gl type enum and data type
        gl_enum, gl_type = type_tuple

        # convert border from True/False to 1/0
        gl_border = 1 if border else 0

        # setup our swizzle
        if gl_swizzle:
            set_swizzle( self.target, gl_swizzle )

        # convert our data 
        # first perform a numpy type conversion
        # then cast to a gl type
        gl_data = (gl_type * len(data))(*data)

        # dynamically set our parameters
        # the only difference in glTex*Image*D
        # functions is the size and optional offsets
        # the offset must be compiled into the size
        # we will unwrap the size into our parameter list
        params = [
            self.target,
            level,
            gl_internal_format
            ] + \
            list(size) + [
            gl_border,
            gl_format,
            gl_enum,
            gl_data
            ]

        # check the alignment of the texture
        alignment = texture_alignment( size )
        if alignment != 4:
            glPixelStorei( GL_UNPACK_ALIGNMENT, alignment )

        # call the function
        func( *params )

        # check if we need to reset our pixel store state
        if alignment != 4:
            glPixelStorei( GL_UNPACK_ALIGNMENT, 4 )


class Texture1D( Texture ):

    def __init__( self, target = GL_TEXTURE_1D ):
        if type(target) is str:
            target = Texture.targets[ target ]

        super( Texture1D, self ).__init__(
            target,
            image_func = glTexImage1D,
            sub_image_func = glTexSubImage1D
            )


class Texture2D( Texture ):

    def __init__( self, target = GL_TEXTURE_2D ):
        if type(target) is str:
            target = Texture.targets[ target ]

        super( Texture2D, self ).__init__(
            target,
            image_func = glTexImage2D,
            sub_image_func = glTexSubImage2D
            )


class Texture3D( Texture ):

    def __init__( self, target = GL_TEXTURE_3D ):
        if type(target) is str:
            target = Texture.targets[ target ]

        super( Texture2D, self ).__init__(
            target,
            image_func = glTexImage3D,
            sub_image_func = glTexSubImage3D
            )


import pkgutil
import os


# make 'from module import *' work dynamically.
# otherwise we have to manually update the __all__ list.
# http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
__all__ = []

for module in os.listdir( os.path.dirname( __file__ ) ):
    name, extension = os.path.splitext( module )

    # don't import ourself
    if name == '__init__':
        continue

    # we can import .py, .pyc and .pyo file types
    extensions = [
        '.py',
        '.pyc',
        '.pyo'
        ]
    if extension not in extensions: 
        continue

    __all__.append( name )
