"""
texture loading helper

shape = (32,32,1)
format = 'luminance'
type = 'uint8'

if gl.is_legacy():
    format = GL_LUMINANCE
else:
    format = GL_RGB
    swizzle = 'rrr'
"""


from OpenGL import GL
from OpenGL.GL.ARB import texture_rg
import numpy

from pyrr.utils import parameters_as_numpy_arrays
import numpy_utils
import gl


def active_unit():
    return GL.glGetInteger(GL.GL_ACTIVE_TEXTURE)

def active_texture(target, unit):
    """Returns the active texture for the specified target and unit.

    .. note:: This requires calls to query and change the
        texture unit.
    """
    # store the currently active unit
    unit_ = active_unit()
    # change to our texture's unit
    if unit_ != unit:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)

    # get the active texture handle
    # TODO:
    # TODO: support more enums
    # TODO:
    query_enums = {
        GL.GL_TEXTURE_1D:   GL.GL_TEXTURE_BINDING_1D,
        GL.GL_TEXTURE_2D:   GL.GL_TEXTURE_BINDING_2D,
        GL.GL_TEXTURE_3D:   GL.GL_TEXTURE_BINDING_3D,
    }
    enum = query_enums[target]
    handle = GL.glGetInteger(enum)

    # restore the active unit
    if unit_ != unit:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit_)

    return handle

def format(format):
    if isinstance(format, basestring):
        # TODO
        pass
    else:
        return format


class Texture(object):
    """Represents an OpenGL texture.
    """

    # TODO:
    # TODO: add the rest of the enum types
    # TODO:

    inferred_targets = {
        1:      GL.GL_TEXTURE_1D,
        2:      GL.GL_TEXTURE_2D,
        3:      GL.GL_TEXTURE_3D,
    }

    target_ndims = {
        GL.GL_TEXTURE_1D:   1,
        GL.GL_TEXTURE_2D:   2,
        GL.GL_TEXTURE_3D:   3,
    }

    inferred_formats = {
        1:      GL.GL_RED,
        2:      texture_rg.GL_RG,
        3:      GL.GL_RGB,
        4:      GL.GL_RGBA,
    }

    funcs = {
        1:      (GL.glTexImage1D, GL.glTexSubImage1D),
        2:      (GL.glTexImage2D, GL.glTexSubImage2D),
        3:      (GL.glTexImage3D, GL.glTexSubImage3D),
    }

    channels = {
        'r':    GL.GL_RED,
        'g':    GL.GL_GREEN,
        'b':    GL.GL_BLUE,
        '1':    GL.GL_ONE,
        '0':    GL.GL_ZERO,
        }

    @classmethod
    def from_file(cls, filename, **kwargs):
        from PIL import Image
        image = Image.open( filename )
        return cls.from_image( image, **kwargs )

    @classmethod
    def from_image(cls, image, **kwargs):
        texture = cls( **kwargs )
        texture.bind()
        texture.set_pil_image(image)
        texture.unbind()
        return texture

    @parameters_as_numpy_arrays('data')
    def __init__(
        self,
        data=None,
        target=None,
        internal_format=None,
        min_filter=GL.GL_NEAREST,
        mag_filter=GL.GL_NEAREST,
        wrap_s=GL.GL_REPEAT,
        wrap_t=GL.GL_REPEAT,
        shape=None,
        format=None,
        data_type=None,
        border=False,
        **kwargs
        ):
        """Creates a new texture.

        By default, only the handle will be allocated.
        Optional parameters allow the texture to be allocated and have data set.

        :param GLuint target: The OpenGL texture target type.
        :param GLuint internal_format: The internal format used by this texture.
        :param GLuint min_filter: The minification filter to use for scaling the image down.
            This MUST be set on OpenGL 3.0+ or the texture won't render.
        :param GLuint mag_filter: The magnification filter to use for scaling the image down.
            This MUST be set on OpenGL 3.0+ or the texture won't render.
        :param GLuint wrap_s: The wrap setting for the S dimension.
        :param GLuint wrap_t: The wrap setting for the T dimension.
        :param bool border: Whether or not to apply a border to the texture.
            This MUST be False on OpenGL 3.0+.
        :param iterable data: Data to set on the texture.
            The data shape should represent the dimensions of the texture and
            the number of channels.

            For example, a 32x32 RGBA texture would have the shape (32,32,4).
        :param tuple shape: Specify the data's shape instead of using the shape of the data variable itself.
        :param GLuint data_type: OpenGL data type (GL_FLOAT, etc).
            Inferred from data dtype if not set.
        :param GLuint format: The OpenGL format of the data.
            Inferred from data shape if not set.
        """
        super(Texture, self).__init__()        

        if data != None:
            # infer any data we haven't be given
            if not target:
                target = Texture.inferred_targets[data.ndims - 1]

            if not shape:
                shape = data.shape[:-1]

            if not data_type:
                data_type = numpy_utils.dtype_gl_enum(data.dtype)

            if not internal_format:
                internal_format = Texture.inferred_formats[data.shape[-1]]

        # TODO: handle target and format being integers or strings
        self._target = target
        self._internal_format = internal_format
        self._handle = GL.glGenTextures(1)
        self._border = border
        self._shape = shape

        self.bind()

        # we should set the min / mag filter now
        # if we don't set it, the texture won't show up in GL 3+
        # and it's a real bitch to debug
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t

        if shape and data_type and internal_format:
            self.allocate(shape, data_type, self._internal_format, **kwargs)

            if data != None:
                self.set_data(data, format=format, shape=shape, data_type=data_type, **kwargs)

        self.unbind()

    @property
    def handle(self):
        return self._handle

    @property
    def target(self):
        return self._target

    @property
    def internal_format(self):
        return self._internal_format

    @property
    def border(self):
        return self._border

    @property
    def shape(self):
        return self._shape

    @property
    def min_filter(self):
        return self._mag_filter

    @min_filter.setter
    def min_filter(self, mode):
        if mode not in [GL.GL_NEAREST, GL.GL_LINEAR, GL.GL_NEAREST_MIPMAP_NEAREST, GL.GL_LINEAR_MIPMAP_NEAREST, GL.GL_NEAREST_MIPMAP_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR]:
            raise ValueError('Invalid texture filter mode')

        self._min_filter = mode
        GL.glTexParameteri(self._target, GL.GL_TEXTURE_MIN_FILTER, mode)

    @property
    def mag_filter(self):
        return self._mag_filter

    @mag_filter.setter
    def mag_filter(self, mode):
        if mode not in [GL.GL_NEAREST, GL.GL_LINEAR, GL.GL_NEAREST_MIPMAP_NEAREST, GL.GL_LINEAR_MIPMAP_NEAREST, GL.GL_NEAREST_MIPMAP_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR]:
            raise ValueError('Invalid texture filter mode')

        self._mag_filter = mode
        GL.glTexParameteri(self._target, GL.GL_TEXTURE_MAG_FILTER, mode)

    @property
    def wrap_s(self):
        return self._wrap_s

    @wrap_s.setter
    def wrap_s(self, mode):
        if mode not in [GL.GL_CLAMP_TO_EDGE, GL.GL_CLAMP_TO_BORDER, GL.GL_MIRRORED_REPEAT, GL.GL_REPEAT]:
            raise ValueError('Invalid wrap mode')

        self._wrap_s = mode
        GL.glTexParameteri(self._target, GL.GL_TEXTURE_WRAP_S, mode)

    @property
    def wrap_t(self):
        return self._wrap_t

    @wrap_t.setter
    def wrap_t(self, mode):
        if mode not in [GL.GL_CLAMP_TO_EDGE, GL.GL_CLAMP_TO_BORDER, GL.GL_MIRRORED_REPEAT, GL.GL_REPEAT]:
            raise ValueError('Invalid wrap mode')

        self._wrap_t = mode
        GL.glTexParameteri(self._target, GL.GL_TEXTURE_WRAP_T, mode)

    def bind(self):
        GL.glBindTexture(self._target, self._handle)

    def unbind(self):
        GL.glBindTexture(self._target, 0)

    def allocate(self, shape, data_type, internal_format=None, **kwargs):
        # assume same format of data
        if not internal_format:
            internal_format = self._internal_format
        else:
            self._internal_format = internal_format

        ndims = Texture.target_ndims[self._target]
        func, _ = Texture.funcs[ndims]

        border = 1 if self._border else 0

        self._shape = tuple(shape)

        if not data_type:
            # attempt to detect the data type from the dtype
            data_type = numpy_utils.dtype_gl_enum(data.dtype)
        else:
            # if we have a dtype
            # determine what type of dtype it is
            if isinstance(data_type, numpy.dtype):
                # numpy dtype
                data_type = numpy_utils.dtype_gl_enum(data_type)
            elif isinstance(data_type, basestring):
                # numpy dtype string
                data_type = numpy_utils.dtype_gl_enum(numpy.dtype(data_type))

        args = [
            self.target,
            0,
            internal_format,] + \
            list(shape) + [
            border,
            GL.GL_RED,  # just use any valid value
            data_type,
            None,
        ]

        func(*args)

    @parameters_as_numpy_arrays('data')
    def set_data(self, data, format=None, shape=None, offset=None, data_type=None, level=0, swizzle=None, **kwargs):
        def set_swizzle(swizzle):
            # sets the swizzle before loading
            # only available on OpenGL Core
            if isinstance(swizzle, (list, tuple)):
                swizzle = (GL.GLint * len(swizzle))(*swizzle)
            elif isinstance(swizzle, basestring):
                result = [
                    Texture.channels[channel]
                    for channel in swizzle.lower()
                ]
                swizzle = (GL.GLint * len(result))(*result)

            GL.glTexParameteriv(self._target, GL.GL_TEXTURE_SWIZZLE_RGBA, swizzle)

        ndims = Texture.target_ndims[self._target]
        _, func = Texture.funcs[ndims]

        if not shape:
            # take the shape from the data
            # but ignore the last dimension
            # this will cause a problem if the data is not in the appropriate shape
            if data.ndims != (ndims + 1):
                raise ValueError('Data must be appropriate shape if shape not specified')
            shape = data.shape[:-1]

        if not offset:
            offset = [0] * ndims

        if not data_type:
            # infer the data type from the numpy dtype
            data_type = numpy_utils.dtype_gl_enum(data.dtype)

        if not format:
            # infer the passed data format using the last dimension of the data
            num_channels = data.shape[-1]
            format = Texture.inferred_formats[num_channels]

        if gl.is_core():
            if swizzle:
                set_swizzle(swizzle)

        args = [
            self.target,
            level,] + \
            list(offset) + \
            list(shape) + [
            format,
            data_type,
            data,
        ]

        func(*args)

    def set_pil_image(self, image, level=0, flip=True, **kwargs):
        # put the formats in functions so they aren't evaluated
        # if they aren't used, this should avoid opengl issues with
        # deprecated formats
        def legacy_format(format):
            return {
                'RGB':  GL.GL_RGB,
                'RGBA': GL.GL_RGBA,
                'RGBX': GL.GL_RGBA,
                'RGBa': GL.GL_RGBA,
                '1':    GL.GL_LUMINANCE,
                'L':    GL.GL_LUMINANCE,
                'LA':   GL.GL_LUMINANCE_ALPHA,
                'F':    GL.GL_LUMINANCE,
                'I':    GL.GL_LUMINANCE,
            }[format]

        def core_format(format):
            return {
                'RGB':  GL.GL_RGB,
                'RGBA': GL.GL_RGBA,
                'RGBX': GL.GL_RGBA,
                'RGBa': GL.GL_RGBA,
                '1':    GL.GL_RED,
                'L':    GL.GL_RED,
                'LA':   texture_rg.GL_RG,
                'F':    GL.GL_RGB,
                'I':    GL.GL_RGB,
            }[format]

        types = {
            'RGB':  ('uint8', GL.GL_RGB8),
            'RGBA': ('uint8', GL.GL_RGBA8),
            'RGBX': ('uint8', GL.GL_RGBA8),
            'RGBa': ('uint8', GL.GL_RGBA8),
            '1':    ('uint8', GL.GL_RGBA8),
            'L':    ('uint8', GL.GL_RGBA8),
            'LA':   ('uint8', GL.GL_RGBA8),
            'F':    ('float32', GL.GL_RGBA32F),
            'I':    ('int32', GL.GL_RGBA32I),
        }

        from PIL import Image

        # TODO: add support for GL_TEXTURE_3D using animated gif / mng
        if self._target != GL.GL_TEXTURE_2D:
            raise ValueError('PIL only supported for GL_TEXTURE_2D')

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
        if image.mode in ['P', 'CMYK', 'YCbCr']:
            image = image.convert('RGBX')

        dtype, internal_format = types[image.mode]
        swizzle = None

        if gl.is_legacy():
            format = legacy_format(image.mode)
        else:
            # core profile doesn't have GL_LUMINANCE
            # instead, use the swizzle method
            format = core_format(image.mode)
            swizzles = {
                '1':    'rrr1',
                'L':    'rrr1',
                'I':    'rrr1',
                'F':    'rrr1',
                'LA':   'rrrg',
            }
            if image.mode in swizzles:
                swizzle = swizzles[image.mode]

        if flip:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        # convert the image to a list
        data = numpy.array(image.getdata(), dtype=dtype)
        data.shape = (image.size[0], image.size[1], -1)

        # allocate the texture
        self.allocate(image.size, dtype, internal_format)

        # send the data
        self.set_data(
            data=data,
            shape=image.size,
            format=format,
            level=level,
            swizzle=swizzle,
            )


class Texture1D(Texture):

    def __init__(self, *args, **kwargs):
        super(Texture1D, self).__init__(target=GL.GL_TEXTURE_1D, *args, **kwargs)

    @property
    def width(self):
        return self._shape[0]


class Texture2D(Texture):

    def __init__(self, *args, **kwargs):
        super(Texture2D, self).__init__(target=GL.GL_TEXTURE_2D, *args, **kwargs)

    @property
    def width(self):
        return self._shape[0]

    @property
    def height(self):
        return self._shape[1]


class Texture3D(Texture):

    def __init__(self, *args, **kwargs):
        super(Texture3D, self).__init__(target=GL.GL_TEXTURE_3D, *args, **kwargs)

    @property
    def width(self):
        return self._shape[0]

    @property
    def height(self):
        return self._shape[1]

    @property
    def depth(self):
        return self._shape[2]

