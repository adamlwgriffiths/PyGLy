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

from pygly.texture import Texture, Texture2D, texture_alignment


def pil_format( image ):
    """Returns the OpenGL enumerations for the
    PIL image mode.
    """
    # convert the image mode into a texture format
    format = {
        'RGB':  'u8/rgb/rgb8',
        'RGBA': 'u8/rgba/rgba8',
        'RGBX': 'u8/rgba/rgba8',
        'RGBa': 'u8/rgba/rgba8',
        '1':    'u8/r/rgba8',
        'L':    'u8/r/rgba8',
        'LA':   'u8/rg/rgba8',
        'F':    'f32/rgb/rgb32f',
        'I':    'i32/rgb/rgb32i',
        }[ image.mode ]

    # check if we need to swizzle the texture
    swizzles = {
        '1':    '/rrr1',
        'L':    '/rrr1',
        'I':    '/rrr1',
        'F':    '/rrr1',
        'LA':   '/rrrg',
        }
    if image.mode in swizzles:
        format += swizzles[ image.mode ]

    return format


def set_pil_image( texture, image, level = 0, border = False, flip = True ):
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
    # convert from unsupported formats to RGBX
    conversion = ['P', 'CMYK', 'YCbCr' ]
    if image.mode in conversion:
        image = image.convert('RGBX')

    # create our format string
    format = pil_format( image )

    # check if we should flip the image
    # we do this because PIL loads images
    # upside down to OpenGL
    # however, this may not be desired sometimes
    if flip:
        image = image.transpose(
            Image.FLIP_TOP_BOTTOM
            )

    # convert the image to a list
    # the list stores each pixel as a tuple
    # so we need to unroll it
    # we also need to handle single channel images
    # that just store ints
    _data = list(image.getdata())
    if type(_data[ 0 ]) is tuple:
        data = [item for sublist in _data for item in sublist]
    else:
        data = _data

    # send the data
    texture.set_image(
        data,
        image.size,
        format,
        level,
        border
        )

