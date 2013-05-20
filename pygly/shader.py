"""Provides Shader and ShaderProgram classes.

Example usage::

    vertex_shader = '''
        VERTEX SHADER TEXT GOES HERE
        '''

    fragment_shader = '''
        FRAGMENT SHADER TEXT GOES HERE
        '''

    # compile and attach our shaders but don't link
    # the program just yet
    shader = ShaderProgram(
        Shader( GL_VERTEX_SHADER, vertex_shader ),
        Shader( GL_FRAGMENT_SHADER, fragment_shader )
        )

    # bind our vertex attributes
    shader.attributes['in_position'] = 0
    shader.attributes['in_normal'].location = 1
    shader.attributes['in_colour'].location = 2

    # bind our fragment output
    shader.frag_location( 'out_frag_colour' )

    # link the shader
    shader.link()

    # set any uniform values that don't change each frame
    shader.bind()

    # uniforms can be accessed directly and a uniform
    # object of the correct type will automatically be
    # created.
    # It is still possible to manually assign them.
    # Although there is no advantage to this as the
    # verification code performs the same steps.
    # here, in_texture_0 will be detected as a sampler
    # variable and an object of type UniformSampler
    # will be created and assigned to it.
    # this allows us to do validation on data passed to the
    # shader's uniforms.
    shader.uniforms['in_texture_0'].value = 0

    shader.unbind()

    # do some other things
    # ...

    # time to render
    # bind the shader
    shader.bind()

    # set our per-frame uniforms
    shader.uniforms['in_time'].value = 1.0

    # render some geometry
    # ...

    # unbind the shader
    shader.unbind()
"""

import numpy
from OpenGL.error import GLError
from OpenGL import GL

from pyrr.utils import parameters_as_numpy_arrays

from pygly.gl import _generate_enum_map


def parse_shader_error( error ):
    """Parses a single GLSL error and extracts the line number
    and error description.

    Line number and description are returned as a tuple.

    GLSL errors are not defined by the standard, as such,
    each driver provider prints their own error format.

    Nvidia print using the following format::

        0(7): error C1008: undefined variable "MV"

    Nouveau Linux driver using the following format::

        0:28(16): error: syntax error, unexpected ')', expecting '('

    ATi and Intel print using the following format::

        ERROR: 0:131: '{' : syntax error parse error
    """
    import re

    # Nvidia
    # 0(7): error C1008: undefined variable "MV"
    match = re.match( r'(\d+)\((\d+)\):\s(.*)', error )
    if match:
        return (
            int(match.group( 2 )),   # line number
            match.group( 3 )    # description
            )

    # ATI
    # Intel
    # ERROR: 0:131: '{' : syntax error parse error
    match = re.match( r'ERROR:\s(\d+):(\d+):\s(.*)', error )
    if match:
        return (
            int(match.group( 2 )),   # line number
            match.group( 3 )    # description
            )

    # Nouveau
    # 0:28(16): error: syntax error, unexpected ')', expecting '('
    match = re.match( r'(\d+):(\d+)\((\d+)\):\s(.*)', error )
    if match:
        return (
            int(match.group( 2 )),   # line number
            match.group( 4 )    # description
            )

    raise ValueError( 'Unknown GLSL error format' )

def parse_shader_errors( errors ):
    """Parses a GLSL error buffer and returns an list of
    error tuples.

    Errors that cannot be parsed will be returned verbatim
    with their line number set to -1.
    """
    results = []
    error_list = errors.split( '\n' )
    for error in error_list:
        try:
            result = parse_shader_error( error )
            results.append( result )
        except ValueError as e:
            results.append( (-1, error) )
    return results

def uniforms( handle ):
    """Returns an iterator for the uniforms of the specified program.

    Each uniform returns a tuple.
    
    :rtype: (name, size, type)
    :return: A tuple consisting of 3 values:
        name is the variable name
        size is the variable size in bytes
        type is the GL enumeration
    """
    # get number of active uniforms
    num_uniforms = GL.glGetProgramiv( handle, GL.GL_ACTIVE_UNIFORMS )

    for index in range( num_uniforms ):
        yield uniform_for_index( handle, index )

def uniform_for_index( handle, index ):
    name, size, type = GL.glGetActiveUniform( handle, index )
    return name, size, type

def uniform_for_name( handle, name ):
    # we can't get uniforms directly
    # we have to iterate over the active uniforms and find our
    # uniform match by the name given
    for uniform in uniforms( handle ):
        _name, _size, _type = uniform

        if _name == name:
            return _name, _size, _type

    # no match found
    return None

def attributes( handle ):
    """Returns an iterator for the attributes of the specified program.

    Each attribute returns a tuple.

    :rtype: (name, size, type)
    :return: A tuple consisting of 3 values:
        name is the variable name
        size is the variable size in bytes
        type is the GL enumeration
    """
    # get number of active uniforms
    num_attributes = GL.glGetProgramiv( handle, GL.GL_ACTIVE_ATTRIBUTES )

    for index in range( num_attributes ):
        yield attribute_for_index( handle, index )

def attribute_for_index( handle, index ):
    """Returns the attribute for the specified attribute index.

    :rtype: tuple(name, size, type)
    """
    # Constants like GLsizei are only found in OpenGL.constants
    # for older versions of pyopengl
    name_length = 30
    glNameSize = (GL.constants.GLsizei)()
    glSize = (GL.constants.GLint)()
    glType = (GL.constants.GLenum)()
    glName = (GL.constants.GLchar * name_length)()

    GL.glGetActiveAttrib(
        handle,
        index,
        name_length,
        glNameSize,
        glSize,
        glType,
        glName
        )

    name, size, type = glName.value, glSize.value, glType.value
    return name, size, type

def attribute_for_name( handle, name ):
    """Returns the attribute for the specified attribute index.

    This iterates over the attributes returned by 
    `py:func:pygly.shader.attribute_for_index`
    until it finds a matching name.

    If no name is found, None is returned.

    :rtype: tuple(name, size, type)
    :return: The attribute tuple or None.
    """
    # we can't get attributes directly
    # we have to iterate over the active attributes and find our
    # attribute match by the name given
    for attribute in attributes( handle ):
        name_, size_, type_ = attribute

        if name_ == name:
            return name_, size_, type_

    # no match found
    return None


#: processes our enumeration to string map and stores the result
_enum_string_map = _generate_enum_map(
    {
        "GL_VERTEX_SHADER":       "GL_VERTEX_SHADER",
        "GL_FRAGMENT_SHADER":     "GL_FRAGMENT_SHADER",
        "GL_GEOMETRY_SHADER":     "GL_GEOMETRY_SHADER",
        "GL_FLOAT":               "GL_FLOAT",
        "GL_FLOAT_VEC2":          "GL_FLOAT_VEC2",
        "GL_FLOAT_VEC3":          "GL_FLOAT_VEC3",
        "GL_FLOAT_VEC4":          "GL_FLOAT_VEC4",
        "GL_INT":                 "GL_INT",
        "GL_INT_VEC2":            "GL_INT_VEC2",
        "GL_INT_VEC3":            "GL_INT_VEC3",
        "GL_INT_VEC4":            "GL_INT_VEC4",
        "GL_UNSIGNED_INT":        "GL_UNSIGNED_INT",
        "GL_UNSIGNED_INT_VEC2":   "GL_UNSIGNED_INT_VEC2",
        "GL_UNSIGNED_INT_VEC3":   "GL_UNSIGNED_INT_VEC3",
        "GL_UNSIGNED_INT_VEC4":   "GL_UNSIGNED_INT_VEC4",
        "GL_UNSIGNED_INT_ATOMIC_COUNTER": "GL_UNSIGNED_INT_ATOMIC_COUNTER",
        "GL_FLOAT_MAT2":          "GL_FLOAT_MAT2",
        "GL_FLOAT_MAT3":          "GL_FLOAT_MAT3",
        "GL_FLOAT_MAT4":          "GL_FLOAT_MAT4",
        "GL_FLOAT_MAT2x3":        "GL_FLOAT_MAT2x3",
        "GL_FLOAT_MAT2x4":        "GL_FLOAT_MAT2x4",
        "GL_FLOAT_MAT3x2":        "GL_FLOAT_MAT3x2",
        "GL_FLOAT_MAT3x4":        "GL_FLOAT_MAT3x4",
        "GL_FLOAT_MAT4x2":        "GL_FLOAT_MAT4x2",
        "GL_FLOAT_MAT4x3":        "GL_FLOAT_MAT4x3",
        "GL_SAMPLER_1D":          "GL_SAMPLER_1D",
        "GL_SAMPLER_2D":          "GL_SAMPLER_2D",
        "GL_SAMPLER_3D":          "GL_SAMPLER_3D",
        "GL_SAMPLER_CUBE":        "GL_SAMPLER_CUBE",
        "GL_SAMPLER_1D_SHADOW":   "GL_SAMPLER_1D_SHADOW",
        "GL_SAMPLER_2D_SHADOW":   "GL_SAMPLER_2D_SHADOW",
        "GL_SAMPLER_1D_ARRAY":    "GL_SAMPLER_1D_ARRAY",
        "GL_SAMPLER_2D_ARRAY":    "GL_SAMPLER_2D_ARRAY",
        "GL_SAMPLER_1D_ARRAY_SHADOW": "GL_SAMPLER_1D_ARRAY_SHADOW",
        "GL_SAMPLER_2D_ARRAY_SHADOW": "GL_SAMPLER_2D_ARRAY_SHADOW",
        "GL_SAMPLER_2D_MULTISAMPLE":  "GL_SAMPLER_2D_MULTISAMPLE",
        "GL_SAMPLER_2D_MULTISAMPLE_ARRAY":    "GL_SAMPLER_2D_MULTISAMPLE_ARRAY",
        "GL_SAMPLER_CUBE_SHADOW": "GL_SAMPLER_CUBE_SHADOW",
        "GL_SAMPLER_BUFFER":      "GL_SAMPLER_BUFFER",
        "GL_SAMPLER_2D_RECT":     "GL_SAMPLER_2D_RECT",
        "GL_SAMPLER_2D_RECT_SHADOW":  "GL_SAMPLER_2D_RECT_SHADOW",
        "GL_INT_SAMPLER_1D":      "GL_INT_SAMPLER_1D",
        "GL_INT_SAMPLER_2D":      "GL_INT_SAMPLER_2D",
        "GL_INT_SAMPLER_3D":      "GL_INT_SAMPLER_3D",
        "GL_INT_SAMPLER_CUBE":    "GL_INT_SAMPLER_CUBE",
        "GL_INT_SAMPLER_1D_ARRAY":    "GL_INT_SAMPLER_1D_ARRAY",
        "GL_INT_SAMPLER_2D_ARRAY":    "GL_INT_SAMPLER_2D_ARRAY",
        "GL_INT_SAMPLER_2D_MULTISAMPLE":  "GL_INT_SAMPLER_2D_MULTISAMPLE",
        "GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY":    "GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
        "GL_INT_SAMPLER_BUFFER":  "GL_INT_SAMPLER_BUFFER",
        "GL_INT_SAMPLER_2D_RECT": "GL_INT_SAMPLER_2D_RECT",
        "GL_UNSIGNED_INT_SAMPLER_1D": "GL_UNSIGNED_INT_SAMPLER_1D",
        "GL_UNSIGNED_INT_SAMPLER_2D": "GL_UNSIGNED_INT_SAMPLER_2D",
        "GL_UNSIGNED_INT_SAMPLER_3D": "GL_UNSIGNED_INT_SAMPLER_3D",
        "GL_UNSIGNED_INT_SAMPLER_CUBE":   "GL_UNSIGNED_INT_SAMPLER_CUBE",
        "GL_UNSIGNED_INT_SAMPLER_1D_ARRAY":   "GL_UNSIGNED_INT_SAMPLER_1D_ARRAY",
        "GL_UNSIGNED_INT_SAMPLER_2D_ARRAY":   "GL_UNSIGNED_INT_SAMPLER_2D_ARRAY",
        "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE": "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE",
        "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY":   "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
        "GL_UNSIGNED_INT_SAMPLER_BUFFER": "GL_UNSIGNED_INT_SAMPLER_BUFFER",
        "GL_UNSIGNED_INT_SAMPLER_2D_RECT":    "GL_UNSIGNED_INT_SAMPLER_2D_RECT",
        "GL_IMAGE_1D":            "GL_IMAGE_1D",
        "GL_IMAGE_2D":            "GL_IMAGE_2D",
        "GL_IMAGE_3D":            "GL_IMAGE_3D",
        "GL_IMAGE_2D_RECT":       "GL_IMAGE_2D_RECT",
        "GL_IMAGE_CUBE":          "GL_IMAGE_CUBE",
        "GL_IMAGE_BUFFER":        "GL_IMAGE_BUFFER",
        "GL_IMAGE_1D_ARRAY":      "GL_IMAGE_1D_ARRAY",
        "GL_IMAGE_2D_ARRAY":      "GL_IMAGE_2D_ARRAY",
        "GL_IMAGE_2D_MULTISAMPLE":    "GL_IMAGE_2D_MULTISAMPLE",
        "GL_IMAGE_2D_MULTISAMPLE_ARRAY":  "GL_IMAGE_2D_MULTISAMPLE_ARRAY",
        "GL_INT_IMAGE_1D":        "GL_INT_IMAGE_1D",
        "GL_INT_IMAGE_2D":        "GL_INT_IMAGE_2D",
        "GL_INT_IMAGE_3D":        "GL_INT_IMAGE_3D",
        "GL_INT_IMAGE_2D_RECT":   "GL_INT_IMAGE_2D_RECT",
        "GL_INT_IMAGE_CUBE":      "GL_INT_IMAGE_CUBE",
        "GL_INT_IMAGE_BUFFER":    "GL_INT_IMAGE_BUFFER",
        "GL_INT_IMAGE_1D_ARRAY":  "GL_INT_IMAGE_1D_ARRAY",
        "GL_INT_IMAGE_2D_ARRAY":  "GL_INT_IMAGE_2D_ARRAY",
        "GL_INT_IMAGE_2D_MULTISAMPLE":    "GL_INT_IMAGE_2D_MULTISAMPLE",
        "GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY":  "GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY",
        "GL_UNSIGNED_INT_IMAGE_1D":   "GL_UNSIGNED_INT_IMAGE_1D",
        "GL_UNSIGNED_INT_IMAGE_2D":   "GL_UNSIGNED_INT_IMAGE_2D",
        "GL_UNSIGNED_INT_IMAGE_3D":   "GL_UNSIGNED_INT_IMAGE_3D",
        "GL_UNSIGNED_INT_IMAGE_2D_RECT":  "GL_UNSIGNED_INT_IMAGE_2D_RECT",
        "GL_UNSIGNED_INT_IMAGE_CUBE": "GL_UNSIGNED_INT_IMAGE_CUBE",
        "GL_UNSIGNED_INT_IMAGE_BUFFER":   "GL_UNSIGNED_INT_IMAGE_BUFFER",
        "GL_UNSIGNED_INT_IMAGE_1D_ARRAY": "GL_UNSIGNED_INT_IMAGE_1D_ARRAY",
        "GL_UNSIGNED_INT_IMAGE_2D_ARRAY": "GL_UNSIGNED_INT_IMAGE_2D_ARRAY",
        "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE":   "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE",
        "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY": "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY",
        }
    )

def enum_to_string( glEnum ):
    """Converts an OpenGL shader uniform or attribute enumeration
    type to a string.

    For example::

        >>> enum_to_string( OpenGL.GL.GL_FLOAT_MAT4 )
        'GL_FLOAT_MAT4'
    """
    global _enum_string_map
    return _enum_string_map[ glEnum ]


class Shader( object ):
    """An individual Shader object.

    Used as part of a single ShaderProgram object.

    A vertex shader (GL_VERTEX_SHADER) and a fragment shader (GL_FRAGMENT_SHADER)
    must be used as part of a single Shader Program.
    Geometry shaders (GL_GEOMETRY_SHADER) are optional.

    Shaders can be used by multiple `py:class:pygly.shader.ShaderProgram`.

    Multiple shaders of the same type can be attached to a ShaderProgram.
    The GLSL linker will over-write any existing functions with the same signature
    with functions from the newly attached shader.
    """

    @classmethod
    def create_from_existing( cls, type, source, handle, compile_now = True ):
        """Creates a Shader object using an existing shader handle
        """
        obj = cls( type, source, False )
        obj._handle = handle
        if compile_now:
            obj.compile()
        return obj

    @classmethod
    def create_from_file( cls, type, filename, compile_now = True ):
        with open(filename) as f:
            return cls( type, f.readlines(), compile_now )

    def __init__( self, type, source, compile_now = True ):
        super( Shader, self ).__init__()

        self._handle = None
        self._type = type
        self._source = source

        if compile_now:
            self.compile()

    @property
    def handle( self ):
        return self._handle

    @property
    def type( self ):
        return self._type

    @property
    def source( self ):
        return self._source

    def compile( self ):
        """Compiles the shader using the current content
        value.

        Shaders are required to be compiled before a
        `py:class:pygly.shader.ShaderProgram` can be linked.

        This is not required to be performed in order to
        attach a Shader to a ShaderProgram. As long as the
        Shader is compiled prior to the ShaderProgram being
        linked.
        """
        self._handle = GL.glCreateShader( self.type )

        GL.glShaderSource( self.handle, self.source )

        # compile the shader
        try:
            GL.glCompileShader( self.handle )
        except GLError as e:
            self._print_shader_errors( e.description )
            raise

        # retrieve the compile status
        if not GL.glGetShaderiv( self.handle, GL.GL_COMPILE_STATUS ):
            errors = GL.glGetShaderInfoLog( self.handle )
            self._print_shader_errors( errors )

            raise GLError( errors )


    def _print_shader_errors( self, buffer ):
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        # print the log to the console
        errors = parse_shader_errors( buffer )
        lines = self.source.split('\n')

        for error in errors:
            line, desc = error

            print( "Error compiling shader type: %s" % enum_to_string( self.type ) )
            print( "\tLine: %i" % line )
            print( "\tDescription: %s" % desc )
            print( "\tCode: %s" % lines[ line - 1 ] )

    def __str__( self ):
        string = "%s(type=%s)" % (
            self.__class__.__name__,
            enum_to_string( self.type )
            )
        return string


class VertexShader( Shader ):
    """An individual Vertex Shader object.

    This is a convenience class that removes the need to pass the
    GL_VERTEX_SHADER type during the construction of a
    `py:class:pygly.shader.Shader` object.
    """

    def __init__( self, *args, **kwargs ):
        super( VertexShader, self ).__init__(
            GL.GL_VERTEX_SHADER, *args, **kwargs
            )


class FragmentShader( Shader ):
    """An individual Fragment Shader object.

    This is a convenience class that removes the need to pass the
    GL_FRAGMENT_SHADER type during the construction of a
    `py:class:pygly.shader.Shader` object.
    """

    def __init__( self, *args, **kwargs ):
        super( FragmentShader, self ).__init__(
            GL.GL_FRAGMENT_SHADER, *args, **kwargs
            )


class ShaderProgram( object ):
    """Defines a complete Shader Program, consisting of at least
    a vertex and fragment shader.
    
    Shader objects are decoupled from ShaderPrograms to avoid recompilation
    when re-using shaders.

    Multiple shaders of the same type can be attached together.
    This lets you combine multiple smaller shaders into a single larger one.

    kwargs supported arguments:
        link_now: defaults to True. If set to True, the shader will be linked
            during the constructor.
        raise_invalid_variables:    defaults to False. If set to True,
            accessing invalid Uniforms and Attributes will trigger a
            ValueError exception to be raised.
    """
    
    def __init__( self, *args, **kwargs ):
        super( ShaderProgram, self ).__init__()

        # create the program handle
        self._handle = GL.glCreateProgram()

        # store our attribute and uniform handler
        self.attributes = Attributes( self )
        self.uniforms = Uniforms( self )

        for shader in args:
            self.attach_shader( shader )

        # default raise exception to False
        self.raise_invalid_variables = kwargs.get(
            'raise_invalid_variables',
            False
            )

        # default link now to True
        link_now = kwargs.get( 'link_now', True )

        if link_now:
            self.link()

    @property
    def handle( self ):
        return self._handle

    def attach_shader( self, shader ):
        """Attaches a Shader object.

        This expects an instance of the Shader class (or equivalent).
        If you need to attach a normal GL shader handle, use the
        Shader.create_from_existing class method to instantiate a
        Shader object first.
        """
        try:
            # attach the shader
            GL.glAttachShader( self.handle, shader.handle )
        except Exception as e:
            print( "Error attaching shader type: %s" % enum_to_string( shader.type ) )
            print( "\tException: %s" % str(e) )

            # chain the exception
            raise

    def frag_location( self, name, buffers = 0 ):
        """Sets the fragment output name used within the program.

        Buffers is the number of buffers receiving the fragment output.
        By default, this is 0.

        Frag data locations MUST be bound BEFORE linking
        or the location will not take effect until
        the shader is linked again!

        http://www.opengl.org/sdk/docs/man3/xhtml/glBindFragDataLocation.xml
        """
        GL.glBindFragDataLocation( self.handle, buffers, name )

    def link( self ):
        """Links the specified shader into a complete program.

        It is important to set any attribute locations and
        the frag data location BEFORE calling link or these calls
        will not take effect.
        """
        # link the program
        try:
            GL.glLinkProgram( self.handle )
        except GLError as e:
            self._print_shader_errors( e.description )
            raise

        # retrieve the compile status
        if not GL.glGetProgramiv( self.handle, GL.GL_LINK_STATUS ):
            errors = GL.glGetProgramInfoLog( self.handle )
            self._print_shader_errors( errors )

            raise GLError( errors )

        self.uniforms._on_program_linked()
        self.attributes._on_program_linked()

    def _print_shader_errors( self, buffer ):
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        print( "Error linking shader:" )
        print( "\tDescription: %s" % ( buffer ) )

        # print the log to the console
        errors = parse_shader_errors( buffer )

        for error in errors:
            line, desc = error

            print( "Error linking shader" )
            print( "\tDescription: %s" % ( desc ) )

    @property
    def linked( self ):
        """Returns the link status of the shader.
        """
        return GL.glGetProgramiv( self.handle, GL.GL_LINK_STATUS ) == GL.GL_TRUE

    def bind( self ):
        """Binds the shader program to be the active shader program.

        The shader MUST be linked for this to be valid.

        It is valid to bind one shader after another without calling
        unbind.
        """
        # bind the program
        GL.glUseProgram( self.handle )

    def unbind( self ):
        """Unbinds the shader program.

        This sets the current shader to null.

        It is valid to bind one shader after another without calling
        unbind.
        Be aware that this will NOT unwind the bind calls.
        Calling unbind will set the active shader to null.
        """
        # unbind the
        GL.glUseProgram( 0 )

    @property
    def bound( self ):
        """Returns True if the program is the currently bound program
        """
        return GL.glGetIntegerv( GL.GL_CURRENT_PROGRAM ) == self.handle

    def __getitem__(self, name):
        """Return the Uniform or Attribute with the specified name.
        """
        if name in self.uniforms.all():
            return self.uniforms[ name ]
        elif name in self.attributes.all():
            return self.attributes[ name ]
        else:
            raise KeyError( name )

    def __str__( self ):
        string = "%s(uniforms=[%s], attributes=[%s])" % (
            self.__class__.__name__,
            str( self.uniforms ),
            str( self.attributes )
            )
        return string


class Uniforms( object ):
    """Provides access to `py:class:pygly.shader.ShaderProgram` uniform variables.

    Uniforms are accessed using array semantics::

        shader.uniforms[ 'model_view' ] = 0
        print( shader.uniforms[ 'model_view' ] )
        >>> 0

    Uniforms provides a mechanism to iterate over the active Uniforms::

        for uniform in shader.uniforms:
            print( uniform )
    """

    """This dictionary holds a list of GL shader enum types.
    Each type has a corresponding Uniform class.
    When processing uniforms, the appropriate class is instantiated
    for the specific time.

    The values are populated by calling
    `py:func:pygly.shader._register_uniform_class`.
    """
    types = {}

    @staticmethod
    def register_uniform_class( cls, types ):
        """Registers a Uniform class to be used for specific GLSL GL types.

        class_type is a class type, such as UniformFloat.
        types is a list of GL enumeration types as strings that the class
        is to be used for.

        For example::

            ['GL_FLOAT_VEC4', 'GL_SAMPLER_1D']

        There is no checking for duplicates, latter calls to this function can over-ride
        existing class registrations.
        """
        for type in types:
            # add to dictionary
            # check if the type is valid
            try:
                Uniforms.types[ getattr(GL, type) ] = cls
            except AttributeError:
                pass

    def __init__( self, program ):
        super( Uniforms, self ).__init__()

        self._program = program
        self._uniforms = {}

    @property
    def program( self ):
        return self._program

    def __iter__( self ):
        return self.next()

    def next( self ):
        for uniform in self.all().values():
            yield uniform

    def _on_program_linked( self ):
        """Called by a ShaderProgram when the program is linked
        successfully.
        """
        # get our active uniforms
        program = self.program
        self._uniforms = {}
        for name, size, type in uniforms( program.handle ):
            self._uniforms[ name ] = self.types[ type ]()
            self._uniforms[ name ]._set_data( program, name, type )

    def all( self ):
        """Returns a dictionary of all uniform objects.

        The key is the uniform name.
        The value is the uniform type as a string.
        Any uniform automatically detected or accessed programmatically
        in python will appear in this list.
        """
        # convert to a list
        return self._uniforms.copy()

    def __getitem__( self, name ):
        """Returns an appropriate uniform for the specified variable name.

        This variable name matches the uniform specified in the shader.

        The ShaderProgram MUST be linked or a ValueError is raised.
        """
        if not self.program.linked:
            raise ValueError( "ShaderProgram must be linked before attribute can be queried" )

        # check if a uniform already exists
        if name in self._uniforms:
            # return the existing uniform
            return self._uniforms[ name ]
        else:
            # the uniform doesn't exit
            # check if we should raise an exception
            # if not, create an InvalidUniform object and store it
            # this means it will only print a log message this one time
            if self.program.raise_invalid_variables:
                raise ValueError( "Uniform '%s' not specified in ShaderProgram" % name )
            else:
                # we shouldn't raise an exception
                # so create an invalid uniform object that will do nothing
                self._uniforms[ name ] = InvalidUniform()
                self._uniforms[ name ]._set_data( self.program, name, type = None )
                return self._uniforms[ name ]

    def __setitem__( self, name, value ):
        """Sets the value of the shader's uniform.

        This lets us just call 'shader.uniforms['variable'] = value'
        """
        self[ name ].value = value

    def __str__( self ):
        string = "%s(" % (self.__class__.__name__)

        for uniform in self:
            string += str(uniform) + ", "
        string = string[:-2] + ")"

        return string


class Uniform( object ):
    """Provides the base class for access to uniform variables.
    """

    def __init__( self, types, dtype ):
        """Creates a new Uniform object.

        This should only be called by inherited Uniform classes.

        Types is a dictionary with the following format:
            key: GL enumeration type as a string, Eg. 'GL_FLOAT_VEC4'.
            value: (uniform setter function, number of values per variable)

        The function is used when setting the uniform value.

        The number of values per variable is used to determine the number of
        variables passed to a uniform.
        Ie. Numver of variables = number of values / values per variable
        """
        super( Uniform, self ).__init__()

        self._types = _generate_enum_map( types )
        self._dtype = dtype

        # these values are set in _set_data which is called by
        # shader.uniforms when an assignment is made
        # this allows users to create uniforms and assign them to
        # a shader
        self._program = None
        self._name = None
        self._type = None
        self._func = None
        self._num_values = None
        self._location = None

    @property
    def name( self ):
        """Returns the name of the uniform as specified in GLSL.

        Eg. in_texture_diffuse
        """
        return self._name

    @property
    def program( self ):
        """Returns the ShaderProgram that owns the Uniform.
        """
        return self._program

    @property
    def location( self ):
        """Returns the location of the Uniform.
        """
        return self._location

    @property
    def type( self ):
        """Returns the GL enumeration type for the Uniform.

        Eg. GL_FLOAT_VEC4.
        """
        return self._type

    @property
    def dtype( self ):
        """Returns the numpy dtype string that represents this Uniform type.

        Eg. "float32"
        """
        return self._dtype

    @property
    def data_size( self ):
        """Returns the number of values that make up a single Uniform.

        Eg, for vec4, this would be 4.
        """
        return self._num_values

    def _set_data( self, program, name, type ):
        """Used by the `py:class:pygly.shader.Uniform` class to pass the data to the Uniform
        object once it is assigned to a ShaderProgram.
        """
        self._program = program
        self._name = name
        self._type = type

        if not self.program.linked:
            raise ValueError( "ShaderProgram must be linked before uniform can be set" )

        # ensure we have the right uniform type
        if self.type not in self._types:
            raise ValueError(
                "Uniform '%s' has type '%s' and is not supported by %s" % (
                    self.name,
                    enum_to_string( self.type ),
                    self.__class__.__name__
                    )
                )

        self._func, self._num_values = self._types[ self.type ]

        # set our location
        self._location = GL.glGetUniformLocation( self.program.handle, self.name )

    @property
    def value( self ):
        """Retrieves the current value of the Uniform.

        .. warning:: Not currently implemented
        """
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        """Assigns a value to the Uniform.
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = self._dtype )

        # check we received the correct number of values
        if 0 != (values.size % self._num_values):
            raise ValueError(
                "Invalid number of values for Uniform, expected multiple of: %d, received: %d" % (
                    self._num_values,
                    values.size
                    )
                )

        count = values.size / self._num_values
        self._func( self.location, count, values )

    def __str__( self ):
        """Returns a human readable string representing the Uniform.
        """
        return "%s(name=%s, type=%s, location=%d)" % (
            self.__class__.__name__,
            self.name,
            enum_to_string( self.type ),
            self.location
            )


class InvalidUniform( Uniform ):
    """Represents an InvalidUniform.

    These are used when exceptions are disabled for invalid uniforms
    and the user attempts to access a uniform that doesn't exist or
    isn't in use.

    If a variable is declared in a GLSL shader but not used in any
    of the code, GLSL will consider it to not exist.
    """

    def __init__( self ):
        super( InvalidUniform, self ).__init__(
            {},
            None
            )

    def _set_data( self, program, name, type ):
        # ensure we have the right uniform type
        print( "Uniform '%s' not specified in ShaderProgram" % name )

    @property
    def value( self ):
        """Always returns None
        """
        return None

    @value.setter
    def value( self, *args ):
        """Stub function that does nothing.
        """
        pass


class UniformFloat( Uniform ):
    """Wraps GLSL Float Uniform types.
    """

    """Defines the accepted Uniform types this object supports.

    The values for each key represent the uniform set function to use
    and the number of expected elements per value.
    """

    #: The types supported by this Uniform class.
    types = {
        "GL_FLOAT":       (GL.glUniform1fv,  1),
        "GL_FLOAT_VEC2":  (GL.glUniform2fv,  2),
        "GL_FLOAT_VEC3":  (GL.glUniform3fv,  3),
        "GL_FLOAT_VEC4":  (GL.glUniform4fv,  4),
        }

    def __init__( self ):
        super( UniformFloat, self ).__init__(
            UniformFloat.types,
            'float32'
            )


class UniformInt( Uniform ):
    """Wraps GLSL Int Uniform types.
    """

    """Defines the accepted Uniform types this object supports.

    The values for each key represent the uniform set function to use
    and the number of expected elements per value.
    """

    #: The types supported by this Uniform class.
    types = {
        "GL_INT":         (GL.glUniform1iv,  1),
        "GL_INT_VEC2":    (GL.glUniform2iv,  2),
        "GL_INT_VEC3":    (GL.glUniform3iv,  3),
        "GL_INT_VEC4":    (GL.glUniform4iv,  4),
        }

    def __init__( self ):
        super( UniformInt, self ).__init__(
            UniformInt.types,
            'int32'
            )


class UniformUint( Uniform ):
    """Wraps GLSL Unsigned Int Uniform types.
    """

    """Defines the accepted Uniform types this object supports.

    The values for each key represent the uniform set function to use
    and the number of expected elements per value.
    """

    #: The types supported by this Uniform class.
    types = {
        "GL_UNSIGNED_INT":        (GL.glUniform1uiv,     1),
        "GL_UNSIGNED_INT_VEC2":   (GL.glUniform2uiv,     2),
        "GL_UNSIGNED_INT_VEC3":   (GL.glUniform3uiv,     3),
        "GL_UNSIGNED_INT_VEC4":   (GL.glUniform4uiv,     4),
        "GL_UNSIGNED_INT_ATOMIC_COUNTER": (GL.glUniform1uiv, 1),
        }

    def __init__( self ):
        super( UniformUint, self ).__init__(
            UniformUint.types,
            'uint32'
            )


class UniformFloatMatrix( Uniform ):
    """Wraps GLSL Float Matrix Uniform types.
    """

    """Defines the accepted Uniform types this object supports.

    The values for each key represent the uniform set function to use
    and the number of expected elements per value.
    """

    #: The types supported by this Uniform class.
    types = {
        "GL_FLOAT_MAT2":      (GL.glUniformMatrix2fv,    4),
        "GL_FLOAT_MAT3":      (GL.glUniformMatrix3fv,    9),
        "GL_FLOAT_MAT4":      (GL.glUniformMatrix4fv,    16),
        "GL_FLOAT_MAT2x3":    (GL.glUniformMatrix2x3fv,  6),
        "GL_FLOAT_MAT2x4":    (GL.glUniformMatrix2x4fv,  8),
        "GL_FLOAT_MAT3x2":    (GL.glUniformMatrix3x2fv,  6),
        "GL_FLOAT_MAT3x4":    (GL.glUniformMatrix3x4fv,  12),
        "GL_FLOAT_MAT4x2":    (GL.glUniformMatrix4x2fv,  8),
        "GL_FLOAT_MAT4x3":    (GL.glUniformMatrix4x3fv,  12),
        }

    def __init__( self ):
        super( UniformFloatMatrix, self ).__init__(
            UniformFloatMatrix.types,
            'float32'
            )

    @Uniform.value.setter
    def value( self, *args ):
        """Sets the matrix values for the uniform.

        This over-ride is required as the matrix methods have an extra
        parameter for transposing a matrix.
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = self._dtype )

        # check we received the correct number of values
        if 0 != (values.size % self._num_values):
            raise ValueError(
                "Invalid number of values for Uniform, expected multiple of: %d, received: %d" % (
                    self._num_values,
                    values.size
                    )
                )

        count = values.size / self._num_values
        self._func( self.location, count, False, values )


class UniformSampler( Uniform ):
    """Wraps GLSL Sampler Uniform types.

    These are the same as UniformInt, but are seperated for convenience.
    """

    """Defines the accepted Uniform types this object supports.

    The values for each key represent the uniform set function to use
    and the number of expected elements per value.
    """

    #: The types supported by this Uniform class.
    types = {
        "GL_SAMPLER_1D":          (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D":          (GL.glUniform1iv,  1),
        "GL_SAMPLER_3D":          (GL.glUniform1iv,  1),
        "GL_SAMPLER_CUBE":        (GL.glUniform1iv,  1),
        "GL_SAMPLER_1D_SHADOW":   (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_SHADOW":   (GL.glUniform1iv,  1),
        "GL_SAMPLER_1D_ARRAY":    (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_ARRAY":    (GL.glUniform1iv,  1),
        "GL_SAMPLER_1D_ARRAY_SHADOW": (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_ARRAY_SHADOW": (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_MULTISAMPLE":  (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_MULTISAMPLE_ARRAY":    (GL.glUniform1iv,  1),
        "GL_SAMPLER_CUBE_SHADOW": (GL.glUniform1iv,  1),
        "GL_SAMPLER_BUFFER":      (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_RECT":     (GL.glUniform1iv,  1),
        "GL_SAMPLER_2D_RECT_SHADOW":  (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_1D":      (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_2D":      (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_3D":      (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_CUBE":    (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_1D_ARRAY":    (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_2D_ARRAY":    (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_2D_MULTISAMPLE":  (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY":    (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_BUFFER":  (GL.glUniform1iv,  1),
        "GL_INT_SAMPLER_2D_RECT": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_1D": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_2D": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_3D": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_CUBE":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_1D_ARRAY":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_2D_ARRAY":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_BUFFER": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_SAMPLER_2D_RECT":    (GL.glUniform1iv,  1),
        "GL_IMAGE_1D":            (GL.glUniform1iv,  1),
        "GL_IMAGE_2D":            (GL.glUniform1iv,  1),
        "GL_IMAGE_3D":            (GL.glUniform1iv,  1),
        "GL_IMAGE_2D_RECT":       (GL.glUniform1iv,  1),
        "GL_IMAGE_CUBE":          (GL.glUniform1iv,  1),
        "GL_IMAGE_BUFFER":        (GL.glUniform1iv,  1),
        "GL_IMAGE_1D_ARRAY":      (GL.glUniform1iv,  1),
        "GL_IMAGE_2D_ARRAY":      (GL.glUniform1iv,  1),
        "GL_IMAGE_2D_MULTISAMPLE":        (GL.glUniform1iv,  1),
        "GL_IMAGE_2D_MULTISAMPLE_ARRAY":  (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_1D":        (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_2D":        (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_3D":        (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_2D_RECT":   (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_CUBE":      (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_BUFFER":    (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_1D_ARRAY":  (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_2D_ARRAY":  (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_2D_MULTISAMPLE":        (GL.glUniform1iv,  1),
        "GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY":  (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_1D":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_2D":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_3D":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_2D_RECT":  (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_CUBE": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_BUFFER":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_1D_ARRAY": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_2D_ARRAY": (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE":   (GL.glUniform1iv,  1),
        "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY": (GL.glUniform1iv,  1),
        }

    def __init__( self ):
        super( UniformSampler, self ).__init__(
            UniformSampler.types,
            'int32'
            )


class Attributes( object ):
    """Provides access to `py:class:pygly.shader.ShaderProgram` attribute bindings.

    Because Attributes must be updated before the shader is linked,
    we cannot do the same validation as we can with Uniforms.

    Attributes are accessed using array semantics::

        shader.attributes[ 'in_position' ] = 0
        print( shader.attributes[ 'in_position' ] )
        >>> 0

    Attributes provides a mechanism to iterate over the active Attributes::

        for attribute in shader.attributes:
            print( attribute )
    """

    def __init__( self, program ):
        super( Attributes, self ).__init__()

        self._program = program
        self._attributes = {}

    @property
    def program( self ):
        return self._program

    def _on_program_linked( self ):
        self._attributes = dict(
            (name, Attribute( self.program, name ))
            for (name, size, type) in attributes( self._program.handle )
            )

    def __iter__( self ):
        return self.next()

    def next( self ):
        for attribute in self.all().values():
            yield attribute

    def all( self ):
        """Returns a dictionary of all the available attributes.

        The key is the attribute name.
        The value is an Attribute object.
        """
        # get number of active attributes
        return self._attributes.copy()

    def __getitem__( self, name ):
        """Returns the currently bound attribute value.

        The ShaderProgram MUST be linked or a ValueError is raised.
        """
        if name not in self._attributes:
            self._attributes[ name ] = Attribute( self.program, name )
        return self._attributes[ name ]

    def __setitem__( self, name, value ):
        """Sets the location of the shader's attribute.

        Passes the value to the attribute's location.
        This lets us just call 'shader.attributes['variable'] = value'

        This value can be set at any time on the `py:class:pygly.shader.ShaderProgram`,
        but it will only take effect the next time the ShaderProgram is linked.
        """
        self[ name ].location = value

    def __str__( self ):
        string = "%s(" % (self.__class__.__name__)

        for attribute in self:
            string += str(attribute) + ", "

        return string[:-2] + ")"


class Attribute( object ):
    """Wraps a GLSL Vertex Attribute.
    """

    def __init__( self, program, name ):
        super( Attribute, self ).__init__()

        self._program = program
        self._name = name

    @property
    def name( self ):
        """Returns the name of the uniform as specified in GLSL.

        Eg. 'in_position'
        """
        return self._name

    @property
    def program( self ):
        """Returns the ShaderProgram that owns the Uniform.
        """
        return self._program

    @property
    def type( self ):
        """Returns the GL enumeration type for the Attribute.

        Eg. GL_FLOAT_VEC4.

        :rtype: GL enumeration or None if invalid.
        """
        attribute = attribute_for_name( self.program.handle, self.name )
        if attribute:
            return attribute[ 2 ]
        return None

    @property
    def location( self ):
        """Returns the location of the Attribute.
        """
        return GL.glGetAttribLocation( self.program.handle, self.name )

    @location.setter
    def location( self, location ):
        """Sets the attributes location.
        """
        GL.glBindAttribLocation( self.program.handle, location, self.name )

    def __str__( self ):
        """Returns a human readable string representing the Attribute.
        """
        return "%s(name=%s, type=%s, location=%d)" % (
            self.__class__.__name__,
            self.name,
            enum_to_string( self.type ),
            self.location
            )


# register our uniform types
def _register_uniforms():
    """Registers our uniform class types with the central
    Uniforms class.

    This is called automatically on import and does not need
    to be called manually.

    Calling this multiple times will not do any harm.
    """
    Uniforms.register_uniform_class( UniformFloat, UniformFloat.types.keys() )
    Uniforms.register_uniform_class( UniformInt, UniformInt.types.keys() )
    Uniforms.register_uniform_class( UniformUint, UniformUint.types.keys() )
    Uniforms.register_uniform_class( UniformFloatMatrix, UniformFloatMatrix.types.keys() )
    Uniforms.register_uniform_class( UniformSampler, UniformSampler.types.keys() )

_register_uniforms()

